#!/usr/bin/env python
# coding=utf-8
import re
import math

# process twitter text
def processTweet(tweet):
    # Convert to lower case
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('"')
    tweet = tweet.strip(',')
    tweet = tweet.strip('.')
    tweet = tweet.strip(':')
    tweet = tweet.strip('!')
    tweet = tweet.strip('?')
    tweet = tweet.strip(')')
    tweet = tweet.strip('(')
    tweet = tweet.strip(';')

    return tweet


# end

def calculateMIScore(feature, tweets):
    # print("--------------------计算--------------------------")
    Y = 0.00
    N = 0.00
    A_Y = 0.00
    A_N = 0.00
    noA_Y = 0.00
    noA_N = 0.00
    for index in range(len(tweets)):
        tweet = tweets[index]
        tweet = processTweet(tweet)
        words = tweet.split()
        if words[1] == "y":
            Y = Y + 1
            if feature[0] in tweet and feature[1] in tweet:
                A_Y = A_Y + 1
            else:
                noA_Y = noA_Y + 1
        else:
            N = N + 1
            if feature[0] in tweet and feature[1] in tweet:
                A_N = A_N + 1
            else:
                noA_N = noA_N + 1
    sum = N + Y
    pY = Y / sum
    pN = N / sum
    pA_Y = A_Y / sum
    pA_N = A_N / sum
    pnoA_Y = noA_Y / sum
    pnoA_N = noA_N / sum
    pA = (A_Y + A_N) / sum
    pnoA = 1 - pA

    # print("p(y)=%s" % (pY))
    # print("p(n)=%s" % (pN))
    # print("p(a,y)=%s" % (pA_Y))
    # print("p(a,n)=%s" % (pA_N))
    # print("p(!a,y)=%s" % (pnoA_Y))
    # print("p(!a,n)=%s" % (pnoA_N))
    # print("p(a)=%s" % (pA))

    pmi_A_Y = 0
    if pA * pA_Y != 0:
        pmi_A_Y = math.log(pA_Y / (pA * pY), 2)

    pmi_noA_Y = 0
    if pnoA * pnoA_Y != 0:
        pmi_noA_Y = math.log(pnoA_Y / (pnoA * pY), 2)

    pmi_A_N = 0
    if pA * pA_N != 0:
        pmi_A_N = math.log(pA_N / (pA * pN), 2)

    pmi_noA_N = 0
    if pnoA * pnoA_N != 0:
        pmi_noA_N = math.log(pnoA_N / (pnoA * pN), 2)

    mi = (pA_Y * pmi_A_Y) + (pnoA_Y * pmi_noA_Y) + (pA_N * pmi_A_N) + (pnoA_N * pmi_noA_N)
    return mi

    # end

# def calculateSingleMIScore(feature, tweets):
#     # print("--------------------计算--------------------------")
#     Y = 0.00
#     N = 0.00
#     A_Y = 0.00
#     A_N = 0.00
#     noA_Y = 0.00
#     noA_N = 0.00
#     for index in range(len(tweets)):
#         tweet = tweets[index]
#         tweet = processTweet(tweet)
#         words = tweet.split()
#         if words[1] == "y":
#             Y = Y + 1
#             if feature in tweet:
#                 A_Y = A_Y + 1
#             else:
#                 noA_Y = noA_Y + 1
#         else:
#             N = N + 1
#             if feature in tweet:
#                 A_N = A_N + 1
#             else:
#                 noA_N = noA_N + 1
#     sum = N + Y
#     pY = Y / sum
#     pN = N / sum
#     pA_Y = A_Y / sum
#     pA_N = A_N / sum
#     pnoA_Y = noA_Y / sum
#     pnoA_N = noA_N / sum
#     pA = (A_Y + A_N) / sum
#     pnoA = 1 - pA

#     # print("p(y)=%s" % (pY))
#     # print("p(n)=%s" % (pN))
#     # print("p(a,y)=%s" % (pA_Y))
#     # print("p(a,n)=%s" % (pA_N))
#     # print("p(!a,y)=%s" % (pnoA_Y))
#     # print("p(!a,n)=%s" % (pnoA_N))
#     # print("p(a)=%s" % (pA))

#     pmi_A_Y = 0
#     if pA * pA_Y != 0:
#         pmi_A_Y = math.log(pA_Y / (pA * pY), 2)

#     pmi_noA_Y = 0
#     if pnoA * pnoA_Y != 0:
#         pmi_noA_Y = math.log(pnoA_Y / (pnoA * pY), 2)

#     pmi_A_N = 0
#     if pA * pA_N != 0:
#         pmi_A_N = math.log(pA_N / (pA * pN), 2)

#     pmi_noA_N = 0
#     if pnoA * pnoA_N != 0:
#         pmi_noA_N = math.log(pnoA_N / (pnoA * pN), 2)

#     mi = (pA_Y * pmi_A_Y) + (pnoA_Y * pmi_noA_Y) + (pA_N * pmi_A_N) + (pnoA_N * pmi_noA_N)
#     return mi

#     # end


if __name__ == '__main__':
    tweetList = []
    tweets = []
    twoGramList = []
    twoGramList2 = []
    resultList = []

    ySet = set()
    nSet = set()

    file = open("train.txt")
    for lines in file:
        tweets.append(lines)
        tweetList.append(processTweet(lines.split("\t")[2].strip()))
    #print tweetList

    for words in tweetList:
        for i in range(0,len(words.split(" "))-1):
            print len(words.split(" ")[i])
            if len(words.split(" ")[i]) > 1 and words.split(" ")[i+1] > 1 :
                theList = [words.split(" ")[i],words.split(" ")[i+1]]
                twoGramList.append(theList)

    for i in twoGramList: 
        if not i in twoGramList2: 
            twoGramList2.append(i) 
    # print twoGramList2
    print len(twoGramList2)

    # for num in range(0,len(twoGramList2)):
    #     result = calculateMIScore(twoGramList2[num],tweets)
    #     print str(num)+" "
    #     print twoGramList2[num]
    #     print result
    #     resultList.append(result)
    # # resultList = []
    # # tokenList = []
    # # trainList = []
    # # for words in tweetList:
    # #     for word in words.split(" "):
    # #         tokenList.append(word)
    # # tokenList = list(set(tokenList))
    # #print tokenList

    # # for word in tokenList:
    # #     result = calculateSingleMIScore(word,tweets)
    # #     print word+"\n"
    # #     print result
    # #     print "\n"
    # #     resultList.append(result)
    
    # print resultList.index(max(resultList))
    # print twoGramList2[resultList.index(max(resultList))]
    # print resultList[resultList.index(max(resultList))]

    

    