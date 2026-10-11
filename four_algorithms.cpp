// C++17. Independent KB, IMPA, Exact, and interleaved Hybrid.
// Exact alone and Exact inside Hybrid use precisely the same runRoot() kernel.
// g is the (verified) girth, and this executable benchmarks T=g only.
#include <bits/stdc++.h>
using namespace std;using ull=unsigned long long;using Clock=chrono::steady_clock;
struct G{
 int n,m,N;vector<vector<int>>a,out;vector<int>from,to,reversePosition;
 explicit G(const string&p){
  ifstream f(p);int E;if(!(f>>n>>m>>E))throw runtime_error("bad graph");
  N=n+m;a.resize(N);out.resize(N);
  for(int i=0,u,v;i<E;i++){
   if(!(f>>u>>v)||u<0||u>=n||v<0||v>=m)throw runtime_error("invalid graph");
   v+=n;int id=from.size();from.push_back(u);to.push_back(v);
   from.push_back(v);to.push_back(u);
   reversePosition.push_back(out[u].size());reversePosition.push_back(out[v].size());
   out[u].push_back(id);out[v].push_back(id+1);a[u].push_back(v);a[v].push_back(u);
  }
 }
};
struct ExactState{
 const G&gr;int g,k,root=0,epoch=0;ull occurrences=0,probes=0;
 vector<int>dist,mark,cnt,nodes,cur,nxt;
 explicit ExactState(const G&gg,int girth):gr(gg),g(girth),k(girth/2),
  dist(gg.N,-1),mark(gg.N),cnt(gg.N){}
 void runRoot(){
  int s=root++;++epoch;nodes.clear();cur.clear();cur.push_back(s);
  nodes.push_back(s);dist[s]=0;
  for(int level=0;level<k-1;level++){
   nxt.clear();for(int u:cur)for(int v:gr.a[u]){
    ++probes;if(dist[v]<0){dist[v]=level+1;nodes.push_back(v);nxt.push_back(v);}
   }cur.swap(nxt);
  }
  for(int u:cur)for(int v:gr.a[u]){
   ++probes;if(dist[v]<0){if(mark[v]!=epoch){mark[v]=epoch;cnt[v]=0;}++cnt[v];}
  }
  for(int u:cur)for(int v:gr.a[u]){
   ++probes;if(mark[v]==epoch){occurrences+=ull(cnt[v])*(cnt[v]-1)/2;mark[v]=0;}
  }
  for(int u:nodes)dist[u]=-1;
 }
 void advance(ull budget){
  ull initial=probes;while(root<gr.n&&probes-initial<budget)runRoot();
 }
 bool done()const{return root==gr.n;}
 ull result()const{
  if(!done()||occurrences%k)throw runtime_error("incomplete exact count");
  return occurrences/k;
 }
};
ull exact(const G&g,int girth){ExactState s(g,girth);s.advance(ULLONG_MAX);return s.result();}
ull kb(const G&gr,int g){
 int D=gr.a[0].size(),E=gr.from.size();
 vector<ull>cur((size_t)E*D),nxt((size_t)E*D),sums((size_t)gr.N*D);
 vector<int>active,an,nodes;vector<char>touched(gr.N);ull result=0;
 for(int root=0;root<gr.n;root++){
  active.clear();for(int j=0;j<(int)gr.out[root].size();j++){
   int e=gr.out[root][j];cur[(size_t)e*D+j]=1;active.push_back(e);
  }
  for(int length=1;length<g;length++){
   nodes.clear();for(int e:active){
    int w=gr.to[e];if(!touched[w]){touched[w]=1;nodes.push_back(w);}
    for(int j=0;j<D;j++)sums[(size_t)w*D+j]+=cur[(size_t)e*D+j];
   }
   an.clear();for(int u:nodes){
    if(u!=root)for(int e:gr.out[u]){
     int w=gr.to[e];if(w<gr.n&&w<root)continue;
     bool nonzero=false;for(int j=0;j<D;j++){
      ull z=sums[(size_t)u*D+j]-cur[(size_t)(e^1)*D+j];
      nxt[(size_t)e*D+j]=z;nonzero|=(z!=0);
     }if(nonzero)an.push_back(e);
    }
   }
   if(length+1==g){
    for(int j=0;j<(int)gr.out[root].size();j++){
     int e=gr.out[root][j]^1;
     for(int h=0;h<D;h++)if(h!=j)result+=nxt[(size_t)e*D+h];
    }
   }
   for(int e:active)for(int j=0;j<D;j++)cur[(size_t)e*D+j]=0;
   for(int u:nodes){touched[u]=0;for(int j=0;j<D;j++)sums[(size_t)u*D+j]=0;}
   cur.swap(nxt);active.swap(an);
  }
  for(int e:active)for(int j=0;j<D;j++)cur[(size_t)e*D+j]=0;
 }
 if(result%2)throw runtime_error("KB parity");return result/2;
}
ull impa(const G&gr,int g){
 int D=gr.a[0].size(),E=gr.from.size();
 vector<ull>cur((size_t)E*D),nxt((size_t)E*D);
 vector<int>active,an,meetnodes;vector<vector<int>>incoming(gr.N);
 vector<char>tagged(E),mtag(gr.N);vector<ull> byLabel(D);ull result=0;
 for(int root=0;root<gr.n;root++){
  active.clear();for(int j=0;j<D;j++){
   int e=gr.out[root][j];cur[(size_t)e*D+j]=1;active.push_back(e);
  }
  for(int p=2;p<=g/2;p++){
   an.clear();for(int e:active){
    int u=gr.to[e];for(int f:gr.out[u]){
     if(f==(e^1))continue;
     int w=gr.to[f];if(w<gr.n&&w<=root)continue;
     if(!tagged[f]){tagged[f]=1;an.push_back(f);}
     for(int j=0;j<D;j++)nxt[(size_t)f*D+j]+=cur[(size_t)e*D+j];
    }
   }
   for(int e:active)for(int j=0;j<D;j++)cur[(size_t)e*D+j]=0;
   if(p==g/2){
    meetnodes.clear();for(int e:an){
     int u=gr.to[e];if(!mtag[u]){mtag[u]=1;meetnodes.push_back(u);}
     incoming[u].push_back(e);
    }
    for(int u:meetnodes){
     auto &es=incoming[u];
     // Small meeting sets: retain the low-overhead direct formula.
     if(es.size()<=5){
      for(int i=0;i<(int)es.size();i++)
       for(int h=i+1;h<(int)es.size();h++)
        for(int a=0;a<D;a++)for(int b=0;b<D;b++)if(a!=b)
         result+=nxt[(size_t)es[i]*D+a]*nxt[(size_t)es[h]*D+b];
     }else{
      // Larger sets: sum distinct-root-label path pairs incrementally.
      // Each unordered pair of incoming edges is counted exactly once.
      ull all=0;
      fill(byLabel.begin(),byLabel.end(),0);
      for(int e:es){
       size_t base=(size_t)e*D;
       for(int a=0;a<D;a++){
        ull x=nxt[base+a];
        result+=x*(all-byLabel[a]);
       }
       for(int a=0;a<D;a++){
        ull x=nxt[base+a];
        byLabel[a]+=x;
        all+=x;
       }
      }
     }
     es.clear();mtag[u]=0;
    }
   }
   for(int e:an)tagged[e]=0;cur.swap(nxt);active.swap(an);
  }
  for(int e:active)for(int j=0;j<D;j++)cur[(size_t)e*D+j]=0;
 }
 return result;
}
struct Sampler{
 const G&gr;int g,r,success=0,start=-1,v=-1,back=-1,depth=0;
 ull trials=0,probes=0;mt19937_64 rng;
 Sampler(const G&gg,int girth,int target,ull seed):
  gr(gg),g(girth),r(target),rng(seed){}
 void advance(ull credits){
  ull used=0;
  while(success<r&&used<credits){
   if(depth==0){start=uniform_int_distribution<int>(0,gr.n-1)(rng);v=start;back=-1;}
   int d=gr.out[v].size();
   int j=uniform_int_distribution<int>(0,d-1-(back>=0))(rng);
   if(back>=0&&j>=back)j++;
   int e=gr.out[v][j];v=gr.to[e];
   back=gr.reversePosition[e^1];depth++;used++;probes++;
   if(depth==g){trials++;success+=(v==start);depth=0;}
  }
 }
};
double Bvalue(const G&gr,int g){
 double dv=gr.a[0].size(),dc=gr.a[gr.n].size();
 return dv*pow(dv-1,g/2-1)*pow(dc-1,g/2);
}
struct HybridResult{double estimate;bool sampled;ull exactops,sampleops;};
HybridResult hybrid(const G&gr,int g,int r,ull seed){
 ExactState ex(gr,g);Sampler sp(gr,g,r,seed);
 double scale=gr.n*Bvalue(gr,g)/g;const ull quantum=8192;
 while(true){
  if(!ex.done())ex.advance(quantum);
  if(ex.done())return {double(ex.result()),false,ex.probes,sp.probes};
  if(sp.success<r)sp.advance(quantum);
  if(sp.success>=r)
   return {scale*(r-1)/double(sp.trials-1),true,ex.probes,sp.probes};
 }
}
template<class F>pair<ull,double>timed(F func,int reps){
 vector<double>v;ull result=0;
 for(int i=0;i<reps;i++){
  auto t=Clock::now();auto z=func();
  double ms=chrono::duration<double,milli>(Clock::now()-t).count();
  if(i&&z!=result)throw runtime_error("nondeterministic count");
  result=z;v.push_back(ms);
 }
 sort(v.begin(),v.end());return {result,v[v.size()/2]};
}
int main(int argc,char**argv){
 try{
  if(argc<3)return 2;G gr(argv[1]);int g=stoi(argv[2]);
  int reps=argc>=4?stoi(argv[3]):7;
  int hrep=argc>=5?stoi(argv[4]):100;
  auto[ng,em]=timed([&](){return exact(gr,g);},reps);
  auto[kn,km]=timed([&](){return kb(gr,g);},reps);
  auto[in,im]=timed([&](){return impa(gr,g);},reps);
  if(kn!=ng||in!=ng)throw runtime_error("COUNTS DISAGREE");
  ExactState verify(gr,g);verify.advance(ULLONG_MAX);
  if(verify.result()!=ng)throw runtime_error("RESUMABLE MISMATCH");
  double avgms=0,mae=0;int randwins=0;
  for(int i=0;i<hrep;i++){
   auto t=Clock::now();auto x=hybrid(gr,g,100,20261012+1009*i);
   avgms+=chrono::duration<double,milli>(Clock::now()-t).count();
   mae+=abs(x.estimate-ng)/ng;randwins+=x.sampled;
  }
  cout<<fixed<<setprecision(8)
   <<"{\"n\":"<<gr.n<<",\"g\":"<<g<<",\"Ng\":"<<ng
   <<",\"KB_ms\":"<<km<<",\"IMPA_ms\":"<<im
   <<",\"Exact_ms\":"<<em<<",\"Hybrid_ms\":"<<avgms/hrep
   <<",\"MARE_percent\":"<<100*mae/hrep
   <<",\"random_wins\":"<<randwins<<",\"reps\":"<<reps
   <<",\"hybrid_reps\":"<<hrep<<"}"<<endl;
 }catch(exception&e){cerr<<"ERROR: "<<e.what()<<"\n";return 1;}
}
