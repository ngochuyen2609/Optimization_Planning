#include <bits/stdc++.h>
using namespace std;

int soKhach, soGhe;
int capacity[23][23];
bool visited[23];
int f_curr = 0;
int f_min = INT_MAX;
int closed[23];
int slot = 0;
int cmin = INT_MAX;

void Try(int stt_curr){
    for(int i = 1; i <= soKhach * 2; i++){
        if( !visited[i] && i <= soKhach && slot < soGhe){//la khach va xe con cho
            visited[i] = true;
            f_curr += capacity[closed[stt_curr - 1]][i];
            closed[stt_curr] = i;
            slot ++;

            Try(stt_curr + 1);

            visited[i] = false;
            f_curr -= capacity[closed[stt_curr - 1]][i];
            slot --;
        }
        else if(!visited[i] && i > soKhach && visited[i - soKhach]){// da don khach -> tra
            visited[i] = true;
            f_curr += capacity[closed[stt_curr - 1]][i];
            closed[stt_curr] = i;
            slot --;

            if(stt_curr < 2 * soKhach  && (f_curr + (2 * soKhach + 1 - stt_curr) * cmin) < f_min){
                Try(stt_curr + 1);
            }else if( stt_curr == 2 * soKhach ){//da di het
                f_min = min(f_min, f_curr + capacity[closed[stt_curr]][0]);
            }
            

            visited[i] = false;
            f_curr -= capacity[closed[stt_curr - 1]][i];
            slot ++;
        }
    }
}
int main(){
    freopen("input.txt","r",stdin);
    freopen("output.txt","w",stdout);
    
    //khach : 1 -> n 
    cin>>soKhach>>soGhe;
    for(int i = 0; i <= 2 * soKhach; i++){
        for(int j = 0; j <= 2 * soKhach; j++){
            cin>>capacity[i][j];
            if(i != j)  cmin = min(cmin, capacity[i][j]);
        }
    }

    closed[0]=0;
    visited[0] = true;
    Try(1);

    cout<<f_min;

    return 0;
}