#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
struct Graph { int n,m; vector<vector<int>> adj; };
Graph load(const string &path){
 ifstream f(path); if(!f)throw runtime_error("cannot open graph");
 int n,m,e; if(!(f>>n>>m>>e)||n<1||m<1||e<1)throw runtime_error("bad header");
 Graph G{n,m,vector<vector<int>>(n+m)};
 for(int i=0,u,v;i<e;++i){
  if(!(f>>u>>v)||u<0||u>=n||v<0||v>=m)throw runtime_error("invalid edge");
  v+=n;G.adj[u].push_back(v);G.adj[v].push_back(u);
 }
 for(auto &a:G.adj){
  sort(a.begin(),a.end());
  if(unique(a.begin(),a.end())!=a.end())throw runtime_error("parallel edges");
 }
 return G;
}
// For a graph known to have girth g=2k, rooted breadth-first search to k-1
// is a tree. Every unordered pair of depth-(k-1) vertices sharing a neighbor
// at depth k gives one g-cycle through that root. Each cycle has k variable roots.
uint64_t exact_girth(const Graph &G,int g){
 if(g<4||g%2)throw runtime_error("even girth required");
 const int k=g/2,N=G.n+G.m;
 vector<int>dist(N,-1),touch,front,next,stamp(N,0),ways(N,0);
 int epoch=0;
 uint64_t sum=0;
 for(int root=0;root<G.n;++root){
  ++epoch;touch.clear();front.clear();front.push_back(root);
  dist[root]=0;touch.push_back(root);
  for(int d=0;d<k-1;++d){
   next.clear();
   for(int u:front)for(int v:G.adj[u]){
    if(dist[v]==-1){dist[v]=d+1;touch.push_back(v);next.push_back(v);}
    else if(dist[v]==d+1)throw runtime_error("graph girth smaller than supplied g");
   }
   front.swap(next);
  }
  for(int u:front)for(int v:G.adj[u])if(dist[v]==-1){
   if(stamp[v]!=epoch){stamp[v]=epoch;ways[v]=0;}
   ++ways[v];
  }
  for(int v:touch)if(dist[v]==k-1)
   for(int w:G.adj[v])if(stamp[w]==epoch){
    sum+=(uint64_t)ways[w]*(ways[w]-1)/2;
    stamp[w]=0;
   }
  for(int u:touch)dist[u]=-1;
 }
 if(sum%k)throw runtime_error("root count not divisible by g/2");
 return sum/k;
}
int main(int argc,char**argv){
 try{
  if(argc!=3){cerr<<"usage: count GRAPH.edges EVEN_GIRTH\n";return 2;}
  Graph G=load(argv[1]);int g=stoi(argv[2]);
  auto start=chrono::steady_clock::now();
  auto n=exact_girth(G,g);
  auto end=chrono::steady_clock::now();
  cout<<"N_g="<<n<<" time_s="<<chrono::duration<double>(end-start).count()<<"\n";
 }catch(exception&e){cerr<<"ERROR: "<<e.what()<<"\n";return 1;}
}
