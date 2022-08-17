import json
import operator

x = "./Settings/moderators.json"
f = open(x, "r")
data = json.load(f)
f.close()
data2 = data["Moderators"]
# Legend:

# 0 = Owner
# 788491002720682004

# 1 = Co-Owner
# 788491004600516639

# 2 = Super Admin
# 788491006337089536

# 3 = Executive Admin
# 837939575459938315

# 4 = Executive Moderator
# 837939575459938315

# 5 = World Admin
# 788491007686737921

# 6 = Discord Admin
# 788491007045664848

# 7 = Discord Moderator
# 944958175864582195

print(data2)
