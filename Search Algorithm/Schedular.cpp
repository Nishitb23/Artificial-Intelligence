#include <bits/stdc++.h>
using namespace std;

pair<float, pair<int, int>> objectiveCal(int *arr, int entry, int *checkRowFull,
        int m, int k, vector<vector<float>> dist, float C) {

    float maxVal = 0;
    int row = 0;
    for (int i = 0; i < m; i++) {

        float fnVal = 0;
        if (!checkRowFull[i]) {
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < k; c++) {
                    if (*((arr + r * m) + c) != 0) {
                        if (r == i) {
                            //calculate similarity
                            fnVal = fnVal + 1- dist[entry - 1][*((arr + r * k) + c) - 1];
                        } else {
                            //calculate distance
                            fnVal = fnVal+ C* dist[entry - 1][*((arr + r * k)+ c) - 1];
                        }

                    }
                }
            }
        }

        if (fnVal > maxVal) {
            maxVal = fnVal;
            row = i;
        }

    }

    int col = 0;
    for (int i = 0; i < k; i++) {
        if (*((arr + row * k) + i) == 0) {
            col = i;
            break;
        }
    }

    pair<int, int> location(row, col);
    pair<float, pair<int, int>> ret(maxVal, location);

    return ret;

}

void optimalSlot(vector<vector<int>> &market, vector<vector<float>> dist,
        vector<int> &shop, int m, int k, int slot, float C) {

    int arr[m][k];

    for (int i = 0; i < m; i++) {
        for (int j = 0; j < k; j++) {
            arr[i][j] = 0;
        }
    }
    int checkRowFull[m] = { 0 };

    int delIndex = rand()%((int) shop.size());
    arr[0][0] = shop[delIndex];
    shop.erase(shop.begin()+delIndex);

    if(k==1){
        checkRowFull[0] = 1;
    }


    int count = 0;
    while (count < k * m - 1) {
        pair<float, pair<int, int>> max;
        int type;
        int index;
        float maxval = 0;
        for (int sp = 0; sp < (int) shop.size(); sp++) {
            pair<float, pair<int, int>> curr = objectiveCal((int*) arr,
                    shop[sp], checkRowFull, m, k, dist, C);
            if (curr.first > maxval) {
                type = shop[sp];
                index = sp;
                max = curr;
                maxval = curr.first;
            }
        }

        pair<int, int> location = max.second;
        arr[location.first][location.second] = type;
        shop.erase(shop.begin() + index);
        if (location.second == k - 1) {
            checkRowFull[location.first] = 1;
        }
        count++;

    }

    for (int i = 0; i < m; i++) {
        for (int j = 0; j < k; j++) {
            market[i][slot * k + j] = arr[i][j];
        }
    }

}

int main() {
    int k,t,m,n;
    float C = 1;
     cin>>k;
     cin>>m;
     cin>>t;
     cin>>C;

     n = k * t * m;

     vector<vector<float>> distance(n);
     for(int i=0;i<n;i++){
         distance[i].resize(n);
     }

     for(int i=0;i<n;i++){
         for(int j=0;j<n;j++){
             cin>> distance[i][j];
         }
     }

    vector<int> shops;
    for (int i = 1; i <= n; i++) {
        shops.push_back(i);
    }

    vector<vector<int>> market(m);
    for (int i = 0; i < m; i++) {
        market[i].resize(k * t);
    }

    for (int i = 0; i < t; i++) {
        optimalSlot(market, distance, shops, m, k, i, C);
    }

    for (int i = 0; i < m; i++) {
        for (int j = 1; j <= k * t; j++) {
            cout << market[i][j - 1] << " ";
            if (j != k * t && j % (k) == 0) {
                cout << "| ";
            }
        }
        cout << endl;
    }
    return 0;
}