#include <iostream>
#include <string>
#include <vector>

std::vector<int> manacher_d1(const std::string &s){
    std::vector<int> d1(s.size());
    int l = 0, r = -1;
    for(int i{}; i < s.size(); i++){
        int k = (i > r) ? 1 : std::min(d1[l + r - i], r - i + 1);
        while(i + k < s.size() && i - k >= 0 && s[i + k] == s[i - k]) k++;
        d1[i] = k--;
        if(i + k > r){
            l = i - k;
            r = i + k;
        }
    }
    return d1;
} 

std::vector<int> manacher_d2(const std::string &s){
    std::vector<int> d2(s.size());
    int l = 0, r = -1;
    for(int i{}; i < s.size(); i++){
        int k = (i > r) ? 0 : std::min(d2[l + r - i + 1], r - i + 1);
        while(i + k < s.size() && i - k - 1 >= 0 && s[i + k] == s[i - k - 1]) k++;
        d2[i] = k--;
        if(i + k > r){
            l = i - k - 1;
            r = i + k;
        }
    }
    return d2;
}

int main(){
    std::string s("abababacababacd");
    std::vector<int> d1 = manacher_d1(s);
    std::vector<int> d2 = manacher_d2(s);
    for(int i{}; i < s.size(); i++){
        std::cout << d1[i] << " ";
    }
    std::cout << std::endl;
    for(int i{}; i < s.size(); i++){
        std::cout << d2[i] << " ";
    }
    return 0;
}