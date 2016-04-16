__author__ = 'Nathan'
#!/usr/bin/env python
import pymysql
import itertools
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import pandas as pd
import seaborn as sns
from matplotlib.pyplot import *
from numpy.random import normal
import statsmodels.api as sm
import statsmodels.formula.api as smf
#from scipy.optimize import curve_fit
#from scipy import stats




def f(x, m, b):
    return a*x+b
    
def func(x, a, b, c, d):
    return a * np.sin(b*x + c) + d
def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]

def main():
    get_gender_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, Male, Female, Other FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
    cursor.execute(get_gender_all_years)
    get_gender_all_years_json = dictfetchall(cursor)
    
    major={}
    females=[]
    years=[]
    termdict={}
    for i in get_gender_all_years_json:
        term = 0
        if "fa" in i['Year']:
            term = int(i['Year'][2:]+"00")
        else:
            term = int(i['Year'][2:]+"00")+50
        if term in termdict.keys():
            termdict[term][i['Major']]=int(i['Female'])
            
        else:
            termdict[term]={}
            termdict[term][i['Major']]=int(i['Female'])
        
        #major.append(i['Major'])
        #termdict[term][i['Major']]=int(i['Female'])
        #females.append(int(i['Female']))
    templist=[]
    
    #for i in termdict.keys():
    #    for j in termdict[i]:
    #        if j == "Computer Science":
    #            print (str(i)+"\t"+str(j)+"\t"+str(termdict[i][j]))
    for i in termdict.keys():
        for j in termdict[i]:
            major[j]=[]
    for i in termdict.keys():
        for j in termdict[i]:
            major[j].append([int(i),int(termdict[i][j])])
    
    yearstemp=[]
    femalestemp=[]
    #print major
    majInf=[]
    for i in major.keys():
        majInf=np.array(major[i])
        year = majInf[:,0] #x
        val = majInf[:,1] #y
        # Encapsulate our test data
        df = pd.DataFrame({'x': year, 'y': val})

        # Implement simple regression: Result ~ Input
        # First we fit slope and intercept
        result = smf.ols(formula='y ~ x', data=df).fit()
        ax = sns.regplot('x', 'y', df, fit_reg=False, color='blue')

        # We pick 100 hundred points equally spaced from the min to the max
        xfpd = pd.DataFrame({'xfpd': np.linspace(0, 1, 50)})

        yfi = result.predict(xfpd)

        plt.plot(xfpd['xfpd'], yfi, color='red', label='y = mx + b')

        ax.set(xlabel='X', ylabel='Y', title='Regression Comparison')
        ax.legend(loc=4)
        sns.despine(offset=0, trim=True)
        plt.show()
       
        #A = np.array([1+0*year, year]).T
        #Q,R = np.linalg.qr(A,"complete")
        #M=np.vander(year)
        #m,n=A.shape
        #x = np.linalg.solve_triangular(R[:n], Q.T.dot(valuse)[:n],lower = False)
        #a_c,b_c = x
        #plt.plot(year,val,'o')
        #plt.plot(x, func(x, *parameter), 'b-', label='fit')
        #plt.show()
        
        #coefficients = np.polyfit(year, val, 6)
        #polynomial = np.poly1d(coefficients)
        #xs = np.arange(min(year), max(year), 0.1)
        #ys = polynomial(xs)

        #plt.plot(year, val, 'o')
        #plt.plot(xs, ys)
        
        #slope, intercept, r_val, p_val, std_err = stats.linregress(year, val)
        #plt.plot(year, f(year, slope, intercept),'b-', label = 'fit')
        #plt.show()

        #parameter, covariance_matrix = curve_fit(func, year, val)

        #x = np.linspace(min(year), max(year), 1000)
        #plt.plot(year, val, 'rx', label='data')
        #plt.plot(x, func(x, *parameter), 'b-', label='fit')   # the star is to unpack the parameter array
        #plt.show()
      
        #print M
        #a= np.linalg.solve(M,val)
        #time = np.linspace(400, 2000, 10)
        #p= np.polyval(a,time)
        #plt.plot(year,val,'o',time,p,'-')
        #plt.show()
        #print year
        #print val
        
    #    for j in major[i]:
    #        print j
    #    for j in i:
    #        print j
        
        
    #print termdict
    
    #regs={}
    #for i in major:
    #    regs[major[[i]]=
        
    


if __name__ == '__main__':
    db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db')
    cursor = db.cursor()
    #runs the main, and prints the time taken to run
    main()