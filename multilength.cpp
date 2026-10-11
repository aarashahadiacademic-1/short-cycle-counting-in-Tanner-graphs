#include <bits/stdc++.h>
using namespace std;using ull=unsigned long long;using Clock=chrono::steady_clock;
struct G{
 int n,m,N,D,E;vector<vector<int>>a,out;vector<int>fr,to;
 G(string fn){ifstream f(fn);int ne; if(!(f>>n>>m>>ne))throw runtime_error("bad graph");N=n+m;a.resize(N);out.resize(N);
 for(int i=0,u,w;i<ne;i++){f>>u>>w;w+=n;int j=fr.size();fr.push_back(u);to.push_back(w);fr.push_back(w);to.push_back(u);a[u].push_back(w);a[w].push_back(u);out[u].push_back(j);out[w].push_back(j+1);}E=fr.size();D=a[0].size();}
};
vector<ull> canonical(const G&Gg,int T){vector<ull>C(T+1);vector<char>seen(Gg.N);for(int root=0;root<Gg.n;root++){
 seen[root]=1;auto dfs=[&](auto&&self,int u,int dep,int first)->void{for(int w:Gg.a[u]){
 if(w==root){if(dep+1>=6&&dep+1<=T&&first<u)++C[dep+1];}
 else if(dep+1<T&&!seen[w]&&(w>=Gg.n||w>root)){seen[w]=1;self(self,w,dep+1,dep==0?w:first);seen[w]=0;}
 }};dfs(dfs,root,0,-1);seen[root]=0;}return C;}
vector<ull> localExact(const G& Gg,int g,int T){
 int N=Gg.N,a=g/2-1,R=T-g+2;
 vector<ull>C(T+1);vector<int>tag(N),dep(N),par(N),branch(N),queue(N);
 vector<char>used(N),blocked(N);int epoch=0;
 for(int v=0;v<Gg.n;v++){
  ++epoch;int qh=0,qt=0;queue[qt++]=v;tag[v]=epoch;dep[v]=0;par[v]=-1;
  while(qh<qt){int z=queue[qh++];if(dep[z]==a)continue;
   for(int w:Gg.a[z])if(tag[w]!=epoch){tag[w]=epoch;dep[w]=dep[z]+1;par[w]=z;branch[w]=(z==v?w:branch[z]);queue[qt++]=w;}
  }
  for(int qi=0;qi<qt;qi++){int x=queue[qi];if(dep[x]!=a)continue;
   for(int z=par[x];z!=-1;z=par[z])blocked[z]=1;
   used[x]=1;
   auto dfs=[&](auto&&self,int z,int l)->void{
    if(l>=2&&!(l&1)&&tag[z]==epoch&&dep[z]==a&&x<z&&branch[x]!=branch[z]){
     bool ok=true;
     for(int w=par[z];w!=-1;w=par[w])if(used[w]){ok=false;break;}
     if(ok)++C[g-2+l];
    }
    if(l==R)return;
    for(int w:Gg.a[z])if(!used[w]&&!blocked[w]){used[w]=1;self(self,w,l+1);used[w]=0;}
   };
   dfs(dfs,x,0);used[x]=0;
   for(int z=par[x];z!=-1;z=par[z])blocked[z]=0;
  }
 }
 for(int t=g;t<=T;t+=2){if((2*C[t])%t)throw runtime_error("Exact divisibility");C[t]=2*C[t]/t;}
 return C;
}
vector<ull> kb(const G& Gg,int g,int T){int D=Gg.D,E=Gg.E;vector<ull>C(T+1),cur((size_t)E*D),nxt((size_t)E*D),sum((size_t)Gg.N*D);vector<int>active,na,nodes;vector<char>touch(Gg.N);
 for(int root=0;root<Gg.n;root++){
 active.clear();for(int j=0;j<D;j++){int e=Gg.out[root][j];cur[(size_t)e*D+j]=1;active.push_back(e);}
 for(int l=1;l<T;l++){
 nodes.clear();for(int e:active){int w=Gg.to[e];if(!touch[w]){touch[w]=1;nodes.push_back(w);}for(int j=0;j<D;j++)sum[(size_t)w*D+j]+=cur[(size_t)e*D+j];}
 na.clear();for(int u:nodes)if(u!=root)for(int e:Gg.out[u]){int z=Gg.to[e];if(z<Gg.n&&z<root)continue;bool nonzero=false;for(int j=0;j<D;j++){ull v=sum[(size_t)u*D+j]-cur[(size_t)(e^1)*D+j];nxt[(size_t)e*D+j]=v;nonzero|=(v!=0);}if(nonzero)na.push_back(e);}
 if((l+1)%2==0&&l+1>=g){for(int j=0;j<D;j++){int e=Gg.out[root][j]^1;for(int k=0;k<D;k++)if(k!=j)C[l+1]+=nxt[(size_t)e*D+k];}}
 for(int e:active)for(int j=0;j<D;j++)cur[(size_t)e*D+j]=0;
 for(int u:nodes){touch[u]=0;for(int j=0;j<D;j++)sum[(size_t)u*D+j]=0;}
 cur.swap(nxt);active.swap(na);
 }
 for(int e:active)for(int j=0;j<D;j++)cur[(size_t)e*D+j]=0;
 }
 for(int t=g;t<=T;t+=2){if(C[t]%2)throw runtime_error("KB parity");C[t]/=2;}return C;}
vector<ull> impa(const G&Gg,int g,int T){int D=Gg.D,E=Gg.E;vector<ull>C(T+1),cur((size_t)E*D),nxt((size_t)E*D),byLabel(D);
 vector<int>active,na,meetnodes;vector<vector<int>>in(Gg.N);vector<char>touched(E),vertexTouched(Gg.N);
 for(int root=0;root<Gg.n;root++){
 active.clear();for(int j=0;j<D;j++){int e=Gg.out[root][j];cur[(size_t)e*D+j]=1;active.push_back(e);}
 for(int p=2;p<=T/2;p++){
 na.clear();for(int e:active){int u=Gg.to[e];for(int f:Gg.out[u]){if(f==(e^1))continue;int w=Gg.to[f];if(w<Gg.n&&w<=root)continue;
 if(!touched[f]){touched[f]=1;na.push_back(f);}for(int j=0;j<D;j++)nxt[(size_t)f*D+j]+=cur[(size_t)e*D+j];}}
 for(int e:active)for(int j=0;j<D;j++)cur[(size_t)e*D+j]=0;
 if(2*p>=g){meetnodes.clear();for(int e:na){int u=Gg.to[e];if(!vertexTouched[u]){vertexTouched[u]=1;meetnodes.push_back(u);}in[u].push_back(e);}
 for(int u:meetnodes){auto&es=in[u];if(es.size()<=5){for(int i=0;i<(int)es.size();i++)for(int h=i+1;h<(int)es.size();h++)for(int j=0;j<D;j++)for(int k=0;k<D;k++)if(j!=k)C[2*p]+=nxt[(size_t)es[i]*D+j]*nxt[(size_t)es[h]*D+k];}
 else {fill(byLabel.begin(),byLabel.end(),0);ull total=0;for(int e:es){size_t b=(size_t)e*D;for(int j=0;j<D;j++)C[2*p]+=nxt[b+j]*(total-byLabel[j]);for(int j=0;j<D;j++){byLabel[j]+=nxt[b+j];total+=nxt[b+j];}}}
 es.clear();vertexTouched[u]=0;}}
 for(int e:na)touched[e]=0;
 cur.swap(nxt);active.swap(na);
 }
 for(int e:active)for(int j=0;j<D;j++)cur[(size_t)e*D+j]=0;
 }
 return C;
}
int main(int argc,char**argv){if(argc<4)return 2;G gg(argv[1]);int g=stoi(argv[2]),T=stoi(argv[3]),reps=argc>4?stoi(argv[4]):7;if(T>=2*g)throw runtime_error("requires T<2g");
 auto time=[&](auto f){vector<double>times;vector<ull>out;for(int i=0;i<reps;i++){auto s=Clock::now();auto z=f(gg,g,T);double t=chrono::duration<double,milli>(Clock::now()-s).count();if(i&&z!=out)throw runtime_error("unstable counts");out=move(z);times.push_back(t);}sort(times.begin(),times.end());return pair<vector<ull>,double>(out,times[reps/2]);};
 auto exact=[&](const G&g,int girth,int t){return localExact(g,girth,t);};
 auto [ref,ex]=time(exact);auto [bk,kt]=time(kb);auto [im,it]=time(impa);auto independent=canonical(gg,T);if(ref!=independent)throw runtime_error("Local exact vs independent canonical DFS mismatch");
 if(ref!=bk||ref!=im){cerr<<"MISMATCH!\n";for(int t=g;t<=T;t+=2)cerr<<t<<":"<<ref[t]<<" "<<bk[t]<<" "<<im[t]<<"\n";return 1;}
 cout<<"{\"n\":"<<gg.n<<",\"g\":"<<g<<",\"T\":"<<T<<",\"N\":[";for(int t=g;t<=T;t+=2){if(t>g)cout<<",";cout<<ref[t];}cout<<"],\"KB_ms\":"<<kt<<",\"IMPA_ms\":"<<it<<",\"Exact_ms\":"<<ex<<"}\n";
}
