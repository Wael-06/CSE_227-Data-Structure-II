#include<bits/stdc++.h>
using namespace std;
#define rep(i,n) for(int i=0;i<(n);i++)
#define all(x) (x).begin(),(x).end()
#define ll int64_t
#define endl '\n'
#define pb push_back
#define INF 1e18

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
	cout.tie(nullptr);

    filesystem::create_directory("arrays");
    
    int n[8] = {500, 1000, 10000, 25000, 50000, 75000, 100000};
    random_device r;
    mt19937 gen(r());

    for (int i : n) {
        vector<int> v(i);
        
        for (int j = 0; j < i; j++) {
            v[j] = gen();
        }

        string input_filename = "n" + to_string(i) + "_input.txt";
        ofstream myfile("arrays/"+input_filename);
        for (int j = 0; j < i; j++) {
            myfile << v[j] << endl;
        }

        sort(v.begin(), v.end());

        string sorted_filename = "n" + to_string(i) + "_sorted.txt";
        ofstream myfile2("arrays/"+sorted_filename);
        for (int j = 0; j < i; j++) {
            myfile2 << v[j] << endl;
        }
    }

    cout << "done" <<endl;

    return 0;
}