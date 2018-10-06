#include <bits/stdc++.h>
using namespace std;
void solve();

int main(){
    freopen("test.in","r",stdin);
    freopen("test.ans","w",stdout);
    ios::sync_with_stdio(0);cin.tie(0);cout.tie(0);
    int T;
    cin>>T;
    while(T--)solve();
}
#define sqr(x) ((x)*(x))
#define f(i,a,b) for(i=a;i<=b;++i)
const int N=1e5+5;
const int K=2;
const int M=2;
int n,k,idx;

struct Node{
    long long x[K];
    bool operator<(const Node&T)const{
        return x[idx]<T.x[idx];
    }
}node[N];
typedef pair<double,Node> PDN;
priority_queue<PDN>que;

class KD_Tree{
public:
    int sz[N*4];
    Node p[N*4];
    void build(int i,int l,int r,int dep){
        if(l>r)return;
        int mid=(l+r)>>1,lc=i<<1,rc=(i<<1)|1;
        idx=dep%k;
        sz[i]=r-l;sz[lc]=sz[rc]=-1;
        nth_element(node+l,node+mid,node+r+1);
        //sort(node+l,node+r+1);
        p[i]=node[mid];
        build(lc,l,mid-1,dep+1);
        build(rc,mid+1,r,dep+1);
    }
    void query(int i,int m,int dep,Node& a){
        if(sz[i]==-1)return;
        PDN tmp=PDN(0,p[i]);
        int j,lc=i<<1,rc=(i<<1)|1,dim=dep%k,flag=0;
        f(j,0,k-1)tmp.first+=sqr(tmp.second.x[j]-a.x[j]);//距离改
        if(a.x[dim]>=p[i].x[dim])swap(lc,rc);	//距离改
        query(lc,m,dep+1,a);
        if(que.size()<m)que.push(tmp);
        else{
                if(tmp.first<que.top().first)que.pop(),que.push(tmp);   //大顶堆，最上面的距离最远
                //if(sqr(a.x[dim]-p[i].x[dim])<que.top().first)flag=1;//距离改
        }
        if(sqr(a.x[dim]-p[i].x[dim])<que.top().first)query(rc,m,dep+1,a);
    }
}KDT;

Node backup[N];
void solve(){
    cin>>n;
    k=2;
    int i;
    f(i,1,n)cin>>node[i].x[0]>>node[i].x[1];
    memcpy(backup,node,sizeof(node));
    KDT.build(1,1,n,0);
    int Q;
    Q=0;
    int m=2;
    while(++Q<=n){
        Node tmp;
        f(i,0,k-1)tmp.x[i]=backup[Q].x[i];
        while(!que.empty())que.pop();
        KDT.query(1,m,0,tmp);
        Node res=que.top().second;
        long long ans=0;
        f(i,0,k-1)ans+=sqr(res.x[i]-tmp.x[i]);
        cout<<ans<<endl;
    }
}
