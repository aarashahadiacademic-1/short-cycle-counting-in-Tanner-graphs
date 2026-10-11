#include <bits/stdc++.h>
using namespace std;
using ull=unsigned long long;
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: multi GRAPH.edges EVEN_MAX_LENGTH\n";return 2;}
 ifstream f(argv[1]);int n,m,E;
 if(!(f>>n>>m>>E))return 2;
 vector<vector<int>> a(n+m);
 for(int u,w;f>>u>>w;){a[u].push_back(n+w);a[n+w].push_back(u);}
 int T=stoi(argv[2]);
 vector<ull> counts(T+1);
 vector<unsigned char> vis(n+m);
 for(int root=0;root<n;root++){
  vis[root]=1;
  auto dfs=[&](auto&&self,int u,int d,int first)->void{
   for(int w:a[u]){
    if(w==root){
     if(d+1>=6&&d+1<=T&&first<u)counts[d+1]++;
    }else if(d+1<T&&!vis[w]&&(w>=n||w>root)){
     vis[w]=1;self(self,w,d+1,d==0?w:first);vis[w]=0;
    }
   }
  };
  dfs(dfs,root,0,-1);vis[root]=0;
 }
 cout<<"n="<<n<<" T="<<T;
 for(int t=6;t<=T;t+=2)cout<<" N"<<t<<"="<<counts[t];
 cout<<"\n";
}
