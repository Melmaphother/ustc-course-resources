#include <iostream>
#include <vector>

int main(){
    int n, k;
    std::cin >> n >> k;
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(k + 1));
    for(int i = 0; i <= n; i++){
        for(int j = 0; j <= k; j++){
            if(i == 0 || j == 0){
				dp[i][j] = 0;
			}else if(i == j){
                dp[i][j] = 1;
            }else if(i < j){
                dp[i][j] = 0;
            }else{
                dp[i][j] = dp[i-1][j-1] + k * dp[i-j][j];
            }
        }
    }
    std::cout << dp[n][k] << std::endl;
    return 0;
}