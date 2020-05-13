import numpy as np
from math import sqrt
from decimal import Decimal
# from absl import logging
import tensorflow as tf
import tensorflow_hub as hub

module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
model = hub.load(module_url)

def embed(input):
  return model(input)

def smartComparison(teacherQuestion, teacherAnswer, studentAnswer, sourceInfo):
    # Define inputs - note: try words, sentences and paragraphs
    # teacherQuestion = 'What causes computer images to be too dark?'
    # teacherAnswer = 'Not all programs will do gamma correction while displaying.'
    # studentAnswer = "A lack of gamma correction when displaying."


    # Generate answers from the model based on the defined inputs above
    answers = sourceInfo.ask(teacherQuestion)


    # Display top 5 results from the answers
    sourceInfo.display_answers(answers[:5])


    # Show the top result in context with input, probability and similarity
    print('Teacher Question:', teacherQuestion)
    print('Teacher Answer:', teacherAnswer)
    print('Student Answer:', studentAnswer)
    computerAnswer = answers[0].get('answer')
    print('Computer Answer:', computerAnswer)
    confidence =  answers[0].get('confidence')
    print('Confidence:', confidence)
    similarity_score =  answers[0].get('similarity_score')
    print('Similarity:', similarity_score)


    # Add all the inputs into an array and embed them into tensors - this is a great example of storing data in higher dimensions :)
    inputArray = [teacherQuestion, teacherAnswer, studentAnswer, computerAnswer]
    inputEmbeddings = embed(inputArray)


    # Enumerate through embeddings and print them for show and tell
    for i, inputEmbeddings in enumerate(np.array(inputEmbeddings).tolist()):
        print("Message: {}".format(inputArray[i]))
        print("Embedding size: {}".format(len(inputEmbeddings)))
        inputEmbeddings = ", ".join(
            (str(x) for x in inputEmbeddings[:3]))
        print("Embedding: [{}, ...]\n".format(inputEmbeddings))
    return inputArray


confidenceThreshold = 0.5

def findSimilarity(correctAnswers, newAnswer):
    # Setup a confidence threshold for calcs lbelow
    confidenceThreshold = 0.5
    # qAndArray = []

    # Defining a class with a bunch of different ways to calculate the distance between two lists.
    class Similarity():
        def euclidean_distance(self,x,y):
            return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

        def manhattan_distance(self,x,y):
            return sum(abs(a-b) for a,b in zip(x,y))

        def minkowski_distance(self,x,y,p_value):
            return self.nth_root(sum(pow(abs(a-b),p_value) for a,b in zip(x, y)),
            p_value)
            
        def nth_root(self,value, n_root):
            root_value = 1/float(n_root)
            return np.round( (Decimal(value) ** Decimal(root_value),3))

        def cosine_similarity(self,x,y):
            numerator = sum(a*b for a,b in zip(x,y))
            denominator = self.square_rooted(x)*self.square_rooted(y)
            return np.round(numerator/float(denominator),3)

        def square_rooted(self,x):
            return np.round(sqrt(sum([a*a for a in x])),3)

    # Put all redundant answer encodings into an array
    def redundant_sent_idx(sim_matrix):
        dup_idx = [] 
        for i in range(sim_matrix.shape[0]):
            if i not in dup_idx:
                tmp = [t+i+1 for t in list(np.where( sim_matrix[i][i+1:] > confidenceThreshold )[0])]
                dup_idx.extend(tmp)
        return dup_idx

    # Embed the input
    # encoding_matrix = embed(qAndArray)

    # Get the index of the similar ones
    # dup_indexes = redundant_sent_idx(np.inner(encoding_matrix,encoding_matrix))

    # Return the value of the similar ones
    # similarAnswers = np.delete(np.array(qAndArray), dup_indexes)

    # Print the similar answers
    # print('Similar Answers:', similarAnswers)

    # Use a function from one of the classes to measure the distance between lists
    # measures = Similarity()
    # newMeasure = measures.cosine_similarity(encoding_matrix[0],encoding_matrix[2])
    # print(newMeasure)

    # Correct Answers
    # correctAnswers = ['Cat', 'Dog', 'Horse']
    correctAnswersMatrix = embed(correctAnswers)

    # Student Answers
    # newAnswer = ['Mouse']
    newAnswerMatrix = embed([newAnswer])

    # Calc the loot
    sim_matrix  = np.inner(newAnswerMatrix, correctAnswersMatrix)
    

    # Print the loot
    if sim_matrix.max() > confidenceThreshold:
        # print('Answer:', newAnswer[0])
        # print("This answer is correct.")
        # print('Max Confidence:', sim_matrix.max())
        return float(sim_matrix.max())
    else:
        # print('Answer:', newAnswer[0])
        # print("This answer is NOT correct.")
        # print('Max Confidence Score:', sim_matrix.max())
        return float(sim_matrix.max())

def testSmartComp():
    from sklearn.datasets import fetch_20newsgroups
    remove = ('headers', 'footers', 'quotes')
    newsgroups_train = fetch_20newsgroups(subset='train', remove=remove)
    newsgroups_test = fetch_20newsgroups(subset='test', remove=remove)
    docs = newsgroups_train.data +  newsgroups_test.data
    INDEXDIR = '/tmp/myindex'
    text.SimpleQA.initialize_index(INDEXDIR)
    text.SimpleQA.index_from_list(docs, INDEXDIR, commit_every=len(docs))
    qa = text.SimpleQA(INDEXDIR)

    smartComparison('What causes computer images to be too dark?', 'Not all programs will do gamma correction while displaying.', "A lack of gamma correction when displaying.", qa)