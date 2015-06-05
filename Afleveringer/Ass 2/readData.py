#!/usr/bin/python2

"""
DBDM Exam 2013 - sqlite example
"""

import sqlite3 as sql
import numpy as np
import matplotlib.pyplot as plot

# open connection to database, create cursor
sqlserver = sql.connect("DataminingAssignment2014.db")
cursor = sqlserver.cursor()

#########
##  1.2
#########
tables = cursor.execute('select * from SSFR_Train_Y').fetchall()

# Set avg var
avg = 0

# sum all y vals
for row in tables:
  avg = avg + row[1]

# find avg
avg /= len(tables)

print 'The average is: ' + repr(avg)

# init bias
bias = 0

# find bias
for row in tables:
    bias = bias + pow((row[1] - avg), 2)

bias /= len(tables)

print '\nThe bias is: ' + repr(bias)

#########
##  1.3
#########

X = np.matrix(cursor.execute("SELECT x1, x2, x3, x4, 1.0 FROM SSFR_Train_X").fetchall())
y = np.matrix(cursor.execute("SELECT y FROM SSFR_Train_Y").fetchall())

w = ((X.T.dot(X)).I.dot(X.T.dot(y)))

print "\nthe model parameters are:\n\n" + str(w)

# Calculate mean square error for the training set

j = 0
for i in xrange(0, len(X)):
    j = j + pow((y[i].T - w.T.dot(X[i].T)),2)

j = float((j / len(X)))

print "\nThe MSE (Mean squared error) for the TRAINING set is: " + str(j)

#Calculate mean square error for the TEST set

X = np.matrix(cursor.execute("SELECT x1, x2, x3, x4, 1.0 FROM SSFR_Test_X").fetchall())
y = np.matrix(cursor.execute("SELECT y FROM SSFR_Test_Y").fetchall())

j = 0
for i in xrange(0, len(X)):
    j = j + pow((y[i].T - w.T.dot(X[i].T)), 2)

j = float((j / (len(X))))

print "\nThe MSE (Mean squared error) for the TEST set is: " + str(j)

#########
##  2.1
#########

#comment out to run classifier

trainingData = cursor.execute("SELECT y, x0, x1, x2, x3, x4, x5, x6, x7, x8, x9 FROM Objects_Train_X AS X_Training NATURAL JOIN Objects_Train_Y AS Y_Training WHERE X_Training.id = Y_Training.id").fetchall()

testData = cursor.execute("SELECT y, x0, x1, x2, x3, x4, x5, x6, x7, x8, x9 FROM Objects_Test_X AS X_Testing NATURAL JOIN Objects_Test_Y AS Y_Testing WHERE X_Testing.id = Y_Testing.id").fetchall()


def NNClassifier(x, data):

    # create the distance, y matrix
    distance_matrix = []
    # loop
    for i, ( y, x0, x1, x2, x3, x4, x5, x6, x7, x8, x9) in enumerate(data):

        # Create a vector with the x values - without Y
        xi = np.array([x0, x1, x2, x3, x4, x5, x6, x7, x8, x9])
        # Calc dist between test and current xi
        dist = np.linalg.norm(  (np.subtract(xi, x)) )

        # append the (dist, y) to the matrix
        distance_matrix.append( [dist, y] )

    distance_matrix = np.matrix(distance_matrix)
    argmin_idx = distance_matrix.argmin(0)
    return int(distance_matrix[argmin_idx[0, 0], 1])

print "Running classification... Will take aprox: forever.. Result is: 0,984666667"

n = 0
for i, (y, x0, x1, x2, x3, x4, x5, x6, x7, x8, x9) in enumerate(testData):
    x_test = np.array((x0, x1, x2, x3, x4, x5, x6, x7, x8, x9))
    if NNClassifier(x_test, trainingData) == y:
        n = n + 1

print str(n) + " / " +  str(len(testData))

########
### 2.2
########

#Step 1 in algorithm 5

S = cursor.execute("SELECT x0, x1, x2, x3, x4, x5, x6, x7, x8, x9 FROM Objects_Train_X AS X_Training, Objects_Train_Y AS Y_Training WHERE X_Training.id = Y_Training.id AND Y_Training.y = 0").fetchall()
S = np.matrix(S).T


#calc empperical / sample mean - step 2 in algorithm 5
mean = []
for x in S:
    mean.append(x.sum())
mean = np.matrix(mean).T
mean = mean / len(S.T)

# step 3 in algorithm 5
e_val, U =  np.linalg.eig(np.cov(S))
p = e_val.argsort()[::-1]
U = U[p]

# Step 4 in algorithm 5 -> finding z
def z(U, mean, x):
    return np.delete(U, np.s_[2::], 1).T * (x - mean)


#Comment out to plot

encoded_lst = []

x, y = z(U, mean, S)
encoded_lst.append((x, y))
xs, ys = zip(*encoded_lst)

plot.plot(e_val)
plot.show()
plot.scatter(xs, ys, color="blue")
plot.show()

# 90% variance
variance = (e_val[0] + e_val[1]) / e_val.sum()
print "2 components necessary to explain variance of: "  + str(variance)

# not working.

# c1 = [np.array([0,0]), np.array([1,1])]
# c2 = [np.array([3,3]), np.array([2,2])]

# while True:
#     l = [[],[]]
#     for dp in np.nditer(z(U, mean, S)):
#         dist = []
#         for c in c2:
#             c = np.array(c)
#             _d = np.linalg.norm((c-dp))
#             dist.append(_d)
#         argmin = np.argmin(dist)
#         l[argmin].append(dp)
#     for i, center in enumerate(c2):
#         dp_some = np.sum(center)
#         dp_some = dp_some/len(c2)
#         c2[i] = dp_some
#     if np.array_equal(c1, c2):
#         break
#     else:
#         c1 = np.copy(c2)

# print c1

# close cursor, connection to database
cursor.close()
sqlserver.close()
