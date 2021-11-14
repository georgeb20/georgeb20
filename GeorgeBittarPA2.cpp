#include <iostream>
#include <string>
#include <fstream>
#include <cmath>
#include <iomanip> 

using namespace std;


//function to print a matrix
void printa(double ** a, int size)
{
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
        {
            cout << a[i][j] << " ";
        }
        cout << endl;
    }
}

int main(int argc, const char *argv[])
{

    //extract file name from argv
    string name = argv[1];

    //initalize size and open the file
    int size=0;
    ifstream inputFile;
    inputFile.open(name.c_str());
    inputFile >> size;

    //initalize 2d array/ a is input matrix (and U matrix)
    double **a = new double*[size];
    int *used = new int[size];
    for(int i=0;i<size;i++)
    {
        a[i] = new double[size];
    }



    //fill 2d array with 0s
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
        {
            inputFile >> a[i][j];
            
        }
    }

    inputFile.close();

    //initalize 2d matrix/ ll is the lower matrix 
    double **ll = new double*[size];
    for(int i=0;i<size;i++)
    {
        ll[i] = new double[size];
    }

    //fill ll matrix with 0s
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
        {
            ll[i][j] = 0;
        }
        
    }

    //initalize p vector - this is the pivot vector
    int *p = new int[size];
    for(int i=0;i<size;i++)
    {
        p[i]=i;
    }

    //initalize variables, max holds max val in col, ind returns the row index of the max in a col
    //s is the scale variable, tmp is used to swap in pivot vector, idk is used to hold max to find scale value
    //pivot is used to bypass used rows in the p vector
    double max=0;
    int ind = 0;
    double s=0;
    int tmp=0;
    int pivot=1;
    double idk=0;
   

    //first for loop walks through the # of columns
    for(int i=0;i<size;i++)
    {
        //initalize max and ind
        max=0;
        ind=-10;

        //second for loop used to walk through rows
        //pivot is used to exclude already used rows
        for(int j=pivot-1;j<size;j++)
        {
            if(fabs(a[p[j]][i])>fabs(max))
            {
                max=fabs(a[p[j]][i]);
                ind=p[j];
            }
        }


        //initalize variable called news
        //news is used to find index of row that needs to be swapped in p
        int news=0;
       for(int y=0;y<size;y++)
       {
           if(ind==p[y])
           {
                news=y;
                break;
           }       
       }

        //now we have the index of the row to swap so we used tmp to swap the row values in p
       tmp=p[i];
       p[i]=ind;
       p[news]=tmp;
        idk = a[p[i]][i];
 
        //set the pivot row and column equal to 1 in the lower matrix
        ll[p[i]][i]=1;

        //third for loop is used to scale the matrix
        //k starts at pivot so we bypass the pivot vector and don't alter it
        for(int k=pivot;k<size;k++)
        {
            //s is calculated for the current pivot vector and column
            s = a[p[k]][i]/idk;
            //s is first stored in lower matrix at the pivot row and column
            ll[p[k]][i]=s;
            //third for loop subtracts the scaled pivot column from the column in a
            for(int z=0;z<size;z++)
            {
                a[p[k]][z]-=a[p[i]][z]*s;
            }
        }

        //increment pivot for next iteration
        pivot++;
        

    }

    //pp is initalized / pp is the P matrix
   double **pp = new double*[size];
    for(int i=0;i<size;i++)
    {
        pp[i] = new double[size];
    }

    //pp is first filled with zeros
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
        {
            pp[i][j]=0;
        }
    }

    //next, we walk through the values in the p vector
    //we check if the value at p[i] is equal to j
    //if it is, we need to place a 1 at p[j][i]
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
        {
            if(p[i]==j)
            {
                pp[p[j]][i] = 1;
            }
        }
        
    }

    //create 3 ofstream objs
    //x is used for U matrix
    //y is used for L matrix
    //z is used for P matrix

    ofstream x,y,z;
    x.open("U.txt");
    y.open("L.txt");
    z.open("P.txt");

    //first output size to all 3 streams
    x << size << endl;
    y << size << endl;
    z << size << endl;


    //next use double for loop to walk through the matrixs
    //i controls the row #
    for(int i=0;i<size;i++)
    {
        //j controls the col #
        for(int j=0;j<size;j++)
        {
            
            //instead of placing the value at M[i][j], we use p[i] to correctly reorder the U and L matrix based on the p vector
            x << setprecision(100) << a[p[i]][j] << " ";
            y << setprecision(100) << ll[p[i]][j] << " ";
            z << setprecision(100) << pp[p[i]][j] << " ";

        }
        //print endl to each stream after each column
        x << endl;
        y << endl;
        z << endl;
    }


    //close each file
    x.close();
    y.close();
    z.close();


    //deallocate memory
    for(int g=0;g<size;g++)
    {
        delete [] a[g];
        delete [] ll[g];
        delete [] pp[g];
    }
    
    delete [] a;
    delete [] ll;
    delete [] pp;

    delete [] p;
  return 0;
}