#include <bits/stdc++.h>
using namespace std;

int client, truck, capacity;
vector<int> d; // khối lượng đơn hàng
vector<vector<int>> c; // chi phí di chuyển
vector<bool> mark; // đánh dấu các khách đã giao hàng
vector<int> first; // first[i]: điểm đầu tiên xe thứ i đi giao hàng
vector<int> nextLocation; // nextLocation[i]: điểm giao tiếp theo sau điểm i
vector<int> load; // load[i]: số lượng hàng trong xe i
int curr_total; // tổng quãng đường hiện tại
int best_total = INT_MAX; // quãng đường nhỏ nhất tìm được
int curr_truck; // số lượng xe thực tế cần dùng
int route; // so duong da di duoc
int dmin = INT_MAX;
int cmin = INT_MAX;

void inputPackage() {
    d.resize(client);
    for (int i = 0; i < client; i++) {
        cin >> d[i];
        dmin = min(dmin, d[i]);

    }
    //cout<<dmin<<endl;
}

// location = 0: depot, location > 0 = client -1
void inputDistance() {
    c.resize(client + 1, vector<int>(client + 1));
    for (int i = 0; i <= client; i++) {
        for (int j = 0; j <= client; j++) {
            cin >> c[i][j];
            if (i != j) cmin = min(cmin, c[i][j]);
        }
    }
    //cout<<cmin<<endl;
}

// kiểm tra xem có thể giao hàng cho khách location không
bool checkNext(int trucki, int location) {
    if (mark[location] == true && location > 0) return false; // khách đã được giao hàng
    if (load[trucki] + d[location - 1] > capacity && location > 0) return false; // quá tải
    return true;
}

// kiểm tra xem location có thể là điểm giao đầu tiên không
//location = 0 : xe tai khong duoc dung den
//location > 0
bool checkFirst(int truck, int location) {
    if(location == 0) return true;
    if (mark[location] == true) return false; // khách đã được giao hàng
    if (load[truck] + d[location - 1] > capacity) return false; // quá tải
    return true;
}

//next cua location
void tryNext(int location, int trucki) {
    if (location == 0) { // xe khong su dung den
        if (trucki < truck - 1) tryNext(first[trucki + 1], trucki + 1);//duyet xe tiep theo
        return;
    }
    for (int i = 0; i <= client; i++) {
        if (checkNext(trucki, i) == true){
            nextLocation[location] = i;
            mark[i] = true;
            curr_total += c[location][i];
            if(i > 0) load[trucki] += d[i -1];
            route ++;

            //cout<<"trucki :"<<trucki<<"next["<<location<<"] = "<< i<<endl;
            if(i > 0 ){
                if( (curr_total + (client + curr_truck - route) * cmin ) < best_total)
                    tryNext(i, trucki);
            }
            else{
                if(trucki == truck -1 ){
                    if(route == client + curr_truck)
                        best_total = min(best_total,curr_total);
                        //cout<<"best_total :"<<best_total<<endl;
                }
                else{
                    if((curr_total + (client + curr_truck - route) * cmin ) < best_total)
                        tryNext(first[trucki + 1], trucki + 1);
                }
            }


            //backtrcking
            mark[i] = false;
            curr_total -= c[location][i];
            if(i > 0) load[trucki] -= d[i-1];
            route --;
        }
    }
}

// Duyệt điểm xuất phát first[truck]
void tryFirst(int trucki) {
    int location = 0; // điểm xuất phát từ depot
    if (first[trucki - 1] >0 && trucki >0) location = first[trucki - 1] + 1;

    for (int i = location; i <= client; i++) {
        if (checkFirst(trucki, i)) {
            first[trucki] = i;
            if(i > 0)  route++;
            mark[i] = true;
            if(i > 0){
                load[trucki] += d[i-1];
                curr_total += c[0][i];
            }
            //cout<<"first["<<trucki<<"] = "<< i<<endl;

            if(trucki < truck - 1) tryFirst(trucki +1);
            else{
                curr_truck =route;
                //cout<< curr_truck<<endl;
                tryNext(first[0],0);
            }

            //backtracking
            if(i > 0)  route--;
            mark[i] = false;
            curr_total -= c[0][i];
            if(i > 0) load[trucki] -= d[i-1];
        }
    }
}

int main() {
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    cin >> client >> truck >> capacity;

    mark.resize(client + 1, false); // khởi tạo đánh dấu
    first.resize(truck + 1, 0); // khởi tạo điểm bắt đầu cho các xe
    nextLocation.resize(client + 1, 0); // khởi tạo điểm tiếp theo
    load.resize(truck + 1, 0); // khởi tạo tải trọng xe

    inputPackage();
    inputDistance();

    tryFirst(0); // bắt đầu với xe đầu tiên

    cout << best_total << endl;

    return 0;
}
