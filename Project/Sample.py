from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(
        self,
        list1: Optional[ListNode],
        list2: Optional[ListNode]
    ) -> Optional[ListNode]:
      
        dummy = ListNode(0)
        cur = dummy

        while list1 and list2:
            if list1.val > list2.val:
                cur.next = list2
                list2 = list2.next
            else:
                cur.next = list1
                list1 = list1.next
            cur = cur.next

        if list1:
            cur.next = list1
        else:
            cur.next = list2
        return dummy.next

# -------- Example Usage --------

# Create list1: 1 -> 2 -> 4
list1 = ListNode(1)
list1.next = ListNode(2)
list1.next.next = ListNode(4)

# Create list2: 1 -> 3 -> 4
list2 = ListNode(1)
list2.next = ListNode(3)
list2.next.next = ListNode(4)

# Merge lists
solution = Solution()
mergedHead = solution.mergeTwoLists(list1, list2)

# Print merged list
current = mergedHead
while current:
    print(current.val, end=" -> ")
    current = current.next
print("null")
