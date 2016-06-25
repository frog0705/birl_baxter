function R = getGripperMatrix(ax,ang)

R = alignToAxAndLevel(ax)*rotAroundZ(ang);

