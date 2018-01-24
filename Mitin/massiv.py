

vm_roles = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [12, 13, 14, 15, 16, 17, 18, 19, 20]]
vm_roles_n = [[], []]

for i in range(len(vm_roles)):
    for k in range(len(vm_roles[i])):
        vm_roles_n[i].append(vm_roles[i][k] * 22)

print vm_roles
print vm_roles_n