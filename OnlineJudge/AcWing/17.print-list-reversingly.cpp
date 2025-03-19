/**
 * @author Cacciatore
 * @version 2025-03-19
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */

class Solution {
public:
    vector<int> printListReversingly(ListNode* head) {
        vector<int> result;

        if (head == nullptr) {
            return result;
        }
        
        stack<int> stk;
        ListNode* current = head;
        while (current) {
            stk.push(current->val);
            current = current->next;
        }

        while (!stk.empty()) {
            result.push_back(stk.top());
            stk.pop();
        }

        return result;
    }
};
