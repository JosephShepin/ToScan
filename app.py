#!/usr/bin/python
# coding=utf-8
from flask import Flask,Response,jsonify, render_template ,flash, redirect, url_for, session,logging,request, make_response, request
app = Flask(__name__)
import urllib
from bs4 import BeautifulSoup
import os

# @app.errorhandler(Exception)
# def all_exception_handler(error):
#    return render_template('form.html')
@app.route('/')
def home():

    return render_template('home.html')




@app.route('/ScanTos', methods = ['GET','POST'])
def TestTos():
    if request.method == 'POST':
        safetyurl = request.form['websiteurl']

        html = urllib.request.urlopen(safetyurl).read()
        soup = BeautifulSoup(html)

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out


        # get text
        text = soup.get_text()


        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)



        ToStr =  text.lower() #Replace 'open("tos.txt", "r").read()' with str
        print(text)
        catagories = ['business-transfers', 'changes', 'tracking', 'waiving-rights']
        negatives = ['not', 'no', 'none', 'never']
        catScore = [0,0,0,0]
        catTotal = [0,0,0,0]
        totalScore = 0
        for i in range(len(catagories)):
            index = i
            terms = [i for i in open("text/"+catagories[i]+".txt", "r").read().replace('_', ' ').split('\n') if i]
            score = 0
            for term in terms:
                current = ToStr.count(term)
                for negative in negatives: #Implement negatives
                    current -= ToStr.count(negative + ' ' + term)
                    current -= ToStr.count(negative + ' be ' + term)
                score+=current
            catTotal[index] = score
            if score<0: score=0
            elif score>25: score=25
            catScore[index] = score
            totalScore += score
        worst = [0,0]
        for i in range(len(catScore)):
            if catScore[i] > worst[0]:
                worst = [catScore[i], i]
        if (100 - (totalScore*3) < 0): totalScore = 0
        else: totalScore = 100 - (totalScore*3)
        # for i in range(4):
        #     print catagories[i].replace("-"," "), "got infracted", catTotal[i], "times."
        zero =  str(catTotal[0])
        one =  str(catTotal[1])
        two =  str(catTotal[2])
        three =  str(catTotal[3])

        recommendations =  'The current ToS has a score of ' + str(totalScore) + ' with the worst being in ' + str(catagories[worst[1]].replace("-"," "))

        print(recommendations)





        # print(ToS)
        score = totalScore
        return render_template('results.html',score = score,recommendations = recommendations,zero=zero,one=one,two=two,three=three,safetyurl=safetyurl)

    else:

        return render_template('form.html')





@app.route('/ScanTosExtention/<string:safetyurl>', methods = ['GET','POST'])
def TestTosExtention(safetyurl):
    safetyurl = "http://" + safetyurl.replace("-slash-","/")
    print(safetyurl)
    html = urllib.request.urlopen(safetyurl).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out


    # get text
    text = soup.get_text()


    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)

    html = urllib.request.urlopen(safetyurl).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out


    # get text
    text = soup.get_text()


    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)



    ToStr =  text.lower() #Replace 'open("tos.txt", "r").read()' with str

    catagories = ['business-transfers', 'changes', 'tracking', 'waiving-rights']
    negatives = ['not', 'no', 'none', 'never',"don't"]
    catScore = [0,0,0,0]
    catTotal = [0,0,0,0]
    totalScore = 0
    for i in range(len(catagories)):
        index = i
        terms = [i for i in open("text/"+catagories[i]+".txt", "r").read().replace('_', ' ').split('\n') if i]
        score = 0
        for term in terms:
            current = ToStr.count(term)
            for negative in negatives: #Implement negatives
                current -= ToStr.count(negative + ' ' + term)
                current -= ToStr.count(negative + ' be ' + term)
            score+=current
        catTotal[index] = score
        if score<0: score=0
        elif score>25: score=25
        catScore[index] = score
        totalScore += score
    worst = [0,0]
    for i in range(len(catScore)):
        if catScore[i] > worst[0]:
            worst = [catScore[i], i]
    if (100 - (totalScore*3) < 0): totalScore = 0
    else: totalScore = 100 - (totalScore*3)
    # for i in range(4):
    #     print catagories[i].replace("-"," "), "got infracted", catTotal[i], "times."
    zero =  str(catTotal[0])
    one =  str(catTotal[1])
    two =  str(catTotal[2])
    three =  str(catTotal[3])


    print(zero)
    print(one)
    print(two)
    print(three)

    recommendations =  'The current ToS has a score of ' + str(totalScore) + ' with the worst being in ' + str(catagories[worst[1]].replace("-"," "))

    print(recommendations)





    # print(ToS)
    score = totalScore
    return render_template('results.html',score = score,recommendations = recommendations,zero=zero,one=one,two=two,three=three, safetyurl=safetyurl)




#run server
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(threaded=True, port=int(os.environ.get("PORT", 5000)))
