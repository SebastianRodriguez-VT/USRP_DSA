"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import time
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0, bands=5, d=2, n=400000, cSteps=10 ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32, np.float32, np.float32, np.float32, np.float32],
            out_sig=[np.float32, np.float32, np.float32, np.float32, np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.counter  = 1
        self.n        = n
        self.bands    = bands
        self.ActionsList = self.SelectOnlyContiguousBands(1)
        self.intf     = [0] * bands
        self.decision = [0] * bands
        self.Reward   = 0
        

        self.k = int((bands * (bands + 1)) / 2) # arms
        self.S = 2 ** (bands)

        
        #d  =  2                #dimensionality
        self.B  =  np.identity(d)   #prior covariance
        self.mu =  [0] * d          #prior mean
        self.f  =  np.transpose([0] * d)  #prior update

        self.cSteps = cSteps
        self.plays  = np.zeros([self.k,self.S])
        self.play2  = np.zeros([self.k,cSteps])

        self.sumR   = self.meanR = self.lastR = np.zeros([self.k,self.S])

        self.loss  = self.col   = np.zeros([1,n])

        self.context =  np.zeros([self.k,d])
        self.armVal  =  np.zeros([self.k,1])

        self.act        = np.zeros([n,bands])
        self.reward     = np.zeros([n,1])
        self.prevAct    = np.ones([1,bands])
        self.expD       = np.zeros([self.k,1])
        self.best       = np.zeros([n,1])
        self.bestArm    = 21

        self.collision       = np.zeros([n,1])
        self.missedO         = np.zeros([n,1])
        self.numSubsSelected = np.zeros([n,1])
        self.state           = self.intf


    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0] * self.example_param
        output_items[1][:] = input_items[1] * self.example_param
        output_items[2][:] = input_items[2] * self.example_param
        output_items[3][:] = input_items[3] * self.example_param
        output_items[4][:] = input_items[4] * self.example_param

        if (output_items[0][0] < 0.77) or (output_items[0][0] > 0.85):
            first = 1
        else:
            first = 0

        if output_items[1][0] > 1.7:
            second = 1
        else:
            second = 0

        if output_items[2][0] > 2.46:
            third = 1
        else:
            third = 0

        if output_items[3][0] > 3.29:
            fourth = 1
        else:
            fourth = 0


        if output_items[4][0] > 4.10:
            fifth = 1

        else:
            fifth = 0
        
        #print(list([first, second, third, fourth, fifth]))

        intf = list([first, second, third, fourth, fifth])
        #decision = self.ThompsonSampling(intf) 
        

        return len(output_items[0])
    

    def NumContiguousOnes(self,a):
        return 0

    def SelectOnlyContiguousBands(self, a):
        print("YEEEEEEEEEEEEEEEEEEEEEEEHAAAAAAAAAAAWWWWWWWWWWW")
        import numpy as np

        bands = 5


        valueList = list([x for x in range(0,(2**bands))])
        finalList = []

        for value in valueList:
            binary = format(value, 'b')
            while len(binary) < bands:
                binary = '0' + binary
            tempList = list([int(x) for x in binary])

            finalList.append(tempList)

        # Now final list has all binary intf values between
        # [0,0,0,0,0] and [1,1,1,1,1]
        finalList.reverse()
        sequence = np.array(finalList[1:len(finalList)])
        # print(sequence)

        NumContigBands = []
        for value in sequence:

            temp = [i+1 for i, e in enumerate(value) if e!= 0]
            temp = [0] + temp + [len(value)+1]
            NumContigBands.append(max(np.diff(temp)-1))
        # print(len(NumContigBands))
        # print(NumContigBands)

        finalList.reverse()

        RowSum = [sum(value) for value in finalList[1:len(finalList)]]
        # print(len(RowSum))
        # print(RowSum)

        IdxContiguousSequences = [1 if NumContigBands[i] == RowSum[i] else 0 for i in range(0,len(IdxContiguousSequences))]

        print(IdxContiguousSequences)
        
        AllContiguousBands = [finalList[i] for i in range(1,len(finalList)-1) if IdxContiguousSequences[i] == 1]
        AllContiguousBands.append([1]*bands)


        #for value in AllContiguousBands:
           # print(value)

        return a + 2
    


    def bi2de(self, number):
        """
        Binary2Decimal
            Python already has some built in functions that let you do this pretty fast. 
            I may just have to swap the order, this would be done by simply changing a 
            +1 to -1

        Number: a list of 5 subbands representing either our action or interferer
        """
        bi2string = ''.join([str(x) for x in number])
        return int(bi2string, 2)



    def de2bi(self, values, bands):
        """
        Decimal2Binary
        """
        valueList = list([x for x in range(0,(2**bands))])
        finalList = []

        for value in valueList:
            binary = format(value, 'b')
            while len(binary) < bands:
                binary = '0' + binary
            tempList = list([int(x) for x in binary])

            finalList.append(tempList)

        return finalList




    def CalculateReward(self, actionTaken, intfSeen): #(fullAct, state, bands)
        """                                           # (decision, intf, bands)
        Take the input and compare it with the interferer seen.
        """
        bFrac = 1/(self.bands)

        cO         = self.intf
        contigOpen = [1-value for value in self.intf]

        stack   = np.add(np.array(cO), np.array(self.decision)) # change this to action
                                                                # Taken Maybe idk yet
        NumCols = sum([1 for value in stack if (value > 1)])
        NB      = sum([value for value in self.decision]) # change this to actionTaken Maybe ######  

        temp = [value == 1 for value in contigOpen]

        f = np.argwhere(np.diff([False] + temp + [False]) == True)

        """
        There must be a better way to do this in python, this feels really inefficient
        """
        #####################################################################
        tempFirst = np.array([list(f[x]) for x in range(1, len(f), 2)])
        tempSecon = np.array([list(f[x]) for x in range(0, len(f), 2)])
        subtraction = np.subtract(tempFirst, tempSecon)
        #####################################################################

        ix = np.argmax(subtraction)
        m  = subtraction[ix]

        runstart = f[(2*ix)]
        longrun  = m
        runEnd   = runstart + longrun

        opt = [0] * self.bands
        for i in range(int(runstart), int(runEnd)):
            opt[i] = 1

        BWdist = np.abs(longrun - NB)

        if NumCols > 0:
            self.Reward = 0
        elif BWdist > 0:
            self.Reward = 1 - (0.1 * BWdist)
        else:
            self.Reward = 1

        if self.Reward < 0:
            self.Reward = 0


        return NumCols



    def ThompsonSampling(self, intf):
        allReward = 0
        print("Hello")
        k = int((self.bands * (self.bands + 1)) / 2) # arms
        print("hello")
        S = 2 ** (self.bands)
        print("HELLO?`")
        """
        TODO: implement this function
        """
        #ActionsList = SelectOnlyContiguousBands(de2bi([1:2^(bands)-1], bands))

        """     
        ********************************************************************
        """


        if self.bands > 10:
            #intfA = np.zeros([len(intf[:,1]),(self.bands-10)])
            #intf = [intf, intfA]
            print("BAND ERROR DONT GO HERE YET")
            raise ValueError("Too many bands, don't do this yet")

        d  =  2                #dimensionality
        B  =  np.identity(d)   #prior covariance
        mu =  [0] * d          #prior mean
        f  =  np.transpose([0] * d)  #prior update

        cSteps = 10
        plays  = np.zeros([k,S])
        play2  = np.zeros([k,cSteps])

        sumR   = np.zeros([k,S])
        meanR  = np.zeros([k,S])
        lastR  = np.zeros([k,S])

        loss  = np.zeros([1,n])
        col   = np.zeros([1,n])

        context =  np.zeros([k,d])
        armVal  =  np.zeros([k,1])

        act        = np.zeros([n,bands])
        reward     = np.zeros([n,1])
        prevAct    = np.ones([1,bands])
        expD       = np.zeros([k,1])
        best       = np.zeros([n,1])
        bestArm    = 21

        collision       = np.zeros([n,1])
        missedO         = np.zeros([n,1])
        numSubsSelected = np.zeros([n,1])
        state           = intf[1]
        #print(state)
        count = 1

        """
        **************************************************************************
        I think everything in between the stars should be implemented at the __init__ 
        section because how else would the function learn unless I constantly passed
        the calculated values back to itself. This way the object keeps track of itself
        **I think**

        If it wasnt pre-initialized I believe that all these lists would have to be 
        stored in work and then recalled at ThompsonSampling(_,_,_,_,_,_,...) again
        """

        




        """
        TODO: this comment
        """
        Sn = bi2de(flip(self.intf))+1







        """#*****************************************************
        Start the Function
        """#*****************************************************

        for t in range(1,n-1):
            #target_range(t+1)  = Vr*PRI(t+1)*t+Ro+cn(t+1);
            theta = np.random.multivariate_normal(mu,np.linalg.inv(B))

            #Calculate posterior index for each arm
            for i in range(0,k-1):
                if (plays(i,Sn) > 0):
                    c1 = meanR[i,Sn] #mean(history(i,Sn,1:plays(i,Sn)));
                    c2 = lastR[i,Sn] #history(i,Sn,plays(i,Sn));
                else:
                    c1 = np.random.uniform()
                    c2 = np.random.uniform()

                context[i,:] = [c1,c2] #arm specific context  
                armVal[i] = np.dot(context[i,:],theta)

            armVal = list(armVal)
            bestArm = int(armVal.index(max(armVal))) #play arm with highest posterior index







            """#*****************************************************
            TODO: this comment
            """#*****************************************************
            #SnP = bi2de(flip(state))+1;
            SnP = 9










            prevState = state

            state = intf[t+1]

            if t == 1:
                count = 1
            elif prevState == state:
                count = count+1
            else :
                count = 1






            """#*****************************************************
            TODO: this comment
            """#*****************************************************
            #Sn = bi2de(flip(state))+1;
            Sn = 10





            plays[bestArm,SnP] = plays[bestArm,SnP]+1

            if count <= cSteps:
                play2[bestArm,count] = play2[bestArm,count] + 1
            else :
                play2[bestArm,cSteps] = play2[bestArm,cSteps] + 1


            best[t-1] = bestArm

            fullAct = ActionsList[bestArm,:]
            act[t,:] = fullAct




            """#*****************************************************
             TODO: this comment
            """#*****************************************************
            #collision[t] = CalculateReward(fullAct,state,bands);
            reward[t] = 0











            allReward = allReward + reward[t]


            sumR[bestArm,SnP] = sumR[bestArm,SnP] + reward[t]
            meanR[bestArm,SnP] = sumR[bestArm,SnP]/plays[bestArm,SnP]
            lastR[bestArm,SnP] = reward[t]
            prevAct = fullAct

            #Update posterior dist
            B = B + np.transpose(context[bestArm,:])*context[bestArm,:]
            f = f + np.transpose(context[bestArm,:])*reward[t]
            mu = f/B

            if t > 1:
                loss[t] = loss[t-1] + (1-reward[t])
                col[t]  = col[t-1]  + collision[t]


        return 0






