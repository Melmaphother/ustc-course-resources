#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>

typedef std::pair<int, int> node;

std::pair<std::vector<int>, int> package(const std::vector<int> &w, const std::vector<int> &v, int W){
    std::vector<std::vector<node>> dp(w.size() + 1, std::vector<node>(W + 1, std::make_pair(0, 0)));
    for(int i{}; i < w.size(); i++){
        for(int j{w[i]}; j <= W; j++){
            if(dp[i][j - w[i]].first + v[i] >= dp[i][j].first){
                dp[i + 1][j] = std::make_pair(dp[i][j - w[i]].first + v[i], j - w[i]);
            }
            else{
                dp[i + 1][j] = std::make_pair(dp[i][j].first, j);
            }
        }
    }
    std::vector<int> res;
    for(int i = w.size(), j{W}; i > 0; i--){
        if(dp[i][j].second < j){
            j = dp[i][j].second;
            res.push_back(i);
        }
    }
    std::reverse(res.begin(), res.end());
    return std::make_pair(res, dp[w.size()][W].first);
}

int package_save_space(const std::vector<int> &w, const std::vector<int> &v, int W){
    std::vector<int> dp(W + 1);
    for(int i{}; i < w.size(); i++){
        for(int j{W}; j >= w[i]; j--){
            dp[j] = std::max(dp[j], dp[j - w[i]] + v[i]);
        }
    }
    return dp[W];
}

int main(){
    std::vector<int> w{2, 1, 3, 2};
    std::vector<int> v{3, 2, 4, 2};
    int W = 5;
    auto dp = package(w, v, W);
    std::cout << dp.second << std::endl;
    for(auto i : dp.first){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    int dp2 = package_save_space(w, v, W);
    std::cout << dp2 << std::endl;
    return 0;
}