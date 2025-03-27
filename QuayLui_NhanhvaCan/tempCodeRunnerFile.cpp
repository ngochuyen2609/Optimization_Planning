#include <bits/stdc++.h>
using namespace std;

int soThanhPho;
int distan[21][21];
int f_curr = 0;
int f_min = INT_MAX;
int dmin = INT_MAX;
bool visited[20];
int closed[20];

void Try(int stt_curr){
    for(int i = 1; i <= soThanhPho; i++){
        if(!visited[i]){
            visited[i] = true;
            closed[stt_curr]=i;
            f_curr += distan[closed[stt_curr - 1]][i];

            if(stt_curr == soThanhPho){
                f_min = min(f_min, f_curr + distan[closed[stt_curr]][closed[1]]);
            }
            if(f_curr + (soThanhPho + 1 - stt_curr)*dmin < f_min)  Try(stt_curr + 1);

            visited[i] = false;
            f_curr -= distan[closed[stt_curr - 1]][i];
        }
    }
}
int main(){
    freopen("input.txt","r",stdin);
    freopen("output.txt","w",stdout);
    
    cin >> soThanhPho;
    memset(distan, 0, sizeof(distan));
    for(int i = 1; i <= soThanhPho; i++){
        for(int j = 1; j <= soThanhPho; j++){
            cin>>distan[i][j];
            if(i != j)dmin =  min(dmin,distan[i][j]);
        }
    }
    
    closed[0]=0;
    Try(1);
    cout<<f_min;

    return 0;
}