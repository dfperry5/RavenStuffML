# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#from PIL import Image
#import numpy
import sys
from PIL import Image, ImageChops

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        sys.setrecursionlimit(10000)
        self.problem_number = 0
        self.TwoX2ChoiceCount = 6
        self.ThreeX3ChoiceCount = 8
        self.answerChoices = []

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        self.Reset()
        self.problem_number += 1
        possibleAnswers = []
        invalidChoices = []
        ABDifference = []
        ABDifferenceKeys = []
        CTestDifference = []

        if problem.problemType == '2x2' and self.problem_number == 5:
            print("Solving Problem #" + str(self.problem_number))
            print("Problem Type: " + problem.problemType)
            print("Has Verbal: " + str(problem.hasVerbal))
            A = problem.figures['A']
            B = problem.figures['B']

            #Step 1:
                # Find Differences in A & B
            abidx = 0
            for objAKey,objAValue in A.objects.items():
                for objBKey, objBValue in B.objects.items():
                    print("=========================")
                    print(objAValue.attributes)
                    print(objBValue.attributes)
                    print("=========================")
                    if len(A.objects.items()) > 1 and len(B.objects.items()) > 1 and set(objAValue.attributes) == set(objBValue.attributes):
                        ABDifference.append(self.findDifference(objAValue, objBValue))
                        # ABDifferenceKeys.append(str(set(objAValue)))
                        print("A-B differences: " + str(ABDifference))
                        abidx = abidx + 1
                    else:
                        ABDifference.append(self.findDifference(objAValue, objBValue))
                        # ABDifferenceKeys.append(str(set(objAValue)))
                        print("A-B differences: " + str(ABDifference))
            
            #Step 2: Get C
            C = problem.figures['C']

            #Step 3: Generate Expected D based on results from A-B Diff:x
        
            #Step 3: Get all Possible Answer Choices
            for i in range(1,self.TwoX2ChoiceCount+1):
                possibleAnswers.append(str(i))
                self.answerChoices.append(problem.figures[str(i)])
            
            #Step 4 - Check all possible answers for ones that have the same difference C That B Does with A.
            answerChoicesCount = 1
            totalDifference = []

            # print(str(ABDifference))
            # print(str(ABDifferenceKeys))

            for testObj in self.answerChoices:
                CTestDifference = []
                for objCKey, objCValue in C.objects.items():
                    for testObjKey, testObjValue in testObj.objects.items():
                        if set(objCValue.attributes) == set(testObjValue.attributes):
                            CTestDifference.append(self.findDifference(objCValue, testObjValue))

                #compare CTdifferences to A-B differences
                print("Now Testing: " + str(self.answerChoices.index(testObj)+1))
                print("CTestDifference: " + str(CTestDifference))
                for abDiff in ABDifference:
                    match = False
                    for ctDiff in CTestDifference:
                        if set(abDiff) == set(ctDiff):
                            print(abDiff)
                            if('angle' in set(abDiff)):
                                print("Trying to find angle diff")
                                abAngleDiff = int(abDiff['angle']['original']) - int(abDiff['angle']['next'])
                                ctAngleDiff = int(ctDiff['angle']['original']) - int(ctDiff['angle']['next'])
                                if( abs(abAngleDiff) == abs(ctAngleDiff)):
                                    match = True
                                else:
                                    match= False
                            else:
                                match = True
                                # print(" A-B Angle Difference!!: " + str(abAngleDiff))
                                # print(" C-T Angle Difference!!: " + str(ctAngleDiff))
                    if not match:
                        if(str(self.answerChoices.index(testObj)+1) not in invalidChoices):
                            # print("The answer is NOT: " + str(self.answerChoices.index(testObj)+1) )
                            possibleAnswers.remove(str(self.answerChoices.index(testObj)+1))
                            invalidChoices.append(str(self.answerChoices.index(testObj)+1))
                answerChoicesCount  = answerChoicesCount + 1
            # print("Possible Answers: " + str(possibleAnswers))
            try:
                if(len(possibleAnswers) > 1):
                    print("More than one possible answer: " + str(possibleAnswers))
                answer = possibleAnswers.pop()
                print("Answer: " + answer)
                return int(answer)
            except:
                return -1

        return -1




           
    #    
    #         for testObj in self.answerChoices:
    #             for objCKey, objCValue in C.objects.items():
    #                 for testObjKey, testObjValue in testObj.objects.items():
    #                     print(testObj.attributes)
    #                     if objCValue.attributes['shape'] == testObjValue.attributes['shape']:
    #                         differences = self.findDifference(objCValue, testObjValue)
    #                         print("C-TestObj Differences: " + str(differences))
    #                         if(differences == constDifferences ):
    #                             print("C-TestObj Differences: " + str(differences))
    #                             # print objCValue.attributes
    #                             # print testObjValue.attributes
    #                             # print differences
    #                             print self.answerChoices.index(testObj) + 1
    #                             return self.answerChoices.index(testObj) + 1
    #         return 0
    #     else:
    #         return 1

    def Reset(self):
        self.answerChoices = []

    def findDifference(self, objA, objB):
        differences = {}
        #NOT ENOUGH DETAILS --- JUST FINDS CATEGORY THAT IS OFF, and matches to that.
        try:
            #Test Shape
            if('shape' in objA.attributes):
                if('shape' in objB.attributes):
                    if('shape' in objA.attributes and 'shape' in objB.attributes and (objA.attributes['shape'] != objB.attributes['shape'])):
                        differences['shape'] = {}
                        differences['shape']['original'] = objA.attributes['shape']
                        differences['shape']['next'] = objB.attributes['shape']
                else:
                    differences['shape'] = {}
                    differences['shape']['original'] = objA.attributes['shape']
                    differences['shape']['next'] = None
            elif('shape' in objB.attributes):
                differences['shape'] = {}
                differences['shape']['original'] = None
                differences['shape']['next'] = objB.attributes['shape']

            #Test Size
            if('size' in objA.attributes):
                if('size' in objB.attributes):
                    if(objA.attributes['size'] != objB.attributes['size']):
                        differences['size'] = {}
                        differences['size']['original'] = objA.attributes['size']
                        differences['size']['next'] = objB.attributes['size']
                else:
                    differences['size'] = {}
                    differences['size']['original'] = objA.attributes['size']
                    differences['size']['next'] = None
            elif('size' in objB.attributes):
                differences['size'] = {}
                differences['size']['original'] = None
                differences['size']['next'] = objB.attributes['size']

            #Test Fill
            if('fill' in objA.attributes):
                if('fill' in objB.attributes):
                    if('fill' in objA.attributes and 'fill' in objB.attributes and (objA.attributes['fill'] != objB.attributes['fill'])):
                        differences['fill'] = {}
                        differences['fill']['original'] = objA.attributes['fill']
                        differences['fill']['next'] = objB.attributes['fill']
                else:
                    differences['fill'] = {}
                    differences['fill']['original'] = objA.attributes['fill']
                    differences['fill']['next'] = None
            elif('fill' in objB.attributes):
                differences['fill'] = {}
                differences['fill']['original'] = None
                differences['fill']['next'] = objB.attributes['fill']

            #Test Inside
            if('inside' in objA.attributes):
                if('inside' in objB.attributes):
                    if('inside' in objA.attributes and 'inside' in objB.attributes and (objA.attributes['inside'] != objB.attributes['inside'])):
                        differences['inside'] = {}
                        differences['inside']['original'] = objA.attributes['inside']
                        differences['inside']['next'] = objB.attributes['inside']
                else:
                    differences['inside'] = {}
                    differences['inside']['original'] = objA.attributes['inside']
                    differences['inside']['next'] = None
            elif('inside' in objB.attributes):
                differences['inside'] = {}
                differences['inside']['original'] = None
                differences['inside']['next'] = objB.attributes['inside']

            #Test ANGLE
            if('angle' in objA.attributes):
                if('angle' in objB.attributes):
                    if('angle' in objA.attributes and 'angle' in objB.attributes and (objA.attributes['angle'] != objB.attributes['angle'])):
                        differences['angle'] = {}
                        differences['angle']['original'] = objA.attributes['angle']
                        differences['angle']['next'] = objB.attributes['angle']
                else:
                    differences['angle'] = {}
                    differences['angle']['original'] = objA.attributes['angle']
                    differences['angle']['next'] = None
            elif('angle' in objB.attributes):
                differences['angle'] = {}
                differences['angle']['original'] = None
                differences['angle']['next'] = objB.attributes['angle']


            #TEST ALIGNMENT
            if('alignment' in objA.attributes):
                if('alignment' in objB.attributes):
                    if('alignment' in objA.attributes and 'alignment' in objB.attributes and (objA.attributes['alignment'] != objB.attributes['alignment'])):
                        differences['alignment'] = {}
                        differences['alignment']['original'] = objA.attributes['alignment']
                        differences['alignment']['next'] = objB.attributes['alignment']
                else:
                    differences['alignment'] = {}
                    differences['alignment']['original'] = objA.attributes['alignment']
                    differences['alignment']['next'] = None
            elif('alignment' in objB.attributes):
                differences['alignment'] = {}
                differences['alignment']['original'] = None
                differences['alignment']['next'] = objB.attributes['alignment']

        except:
            print("FAILURE")
            print("==============================")
            print("A: " + str(objA.attributes))
            print("Name: " + objA.name)
            print("B: " + str(objB.attributes))
            print("Name: " + objB.name)
            print("==============================")
        return differences