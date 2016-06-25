% "Snaps" approach vectors to vertical in cases where they should be. The
% main ones are:
%
% 1) Rectangle oriented almost vertically - in most cases, this means we
% detected a grasp across the rim of something, or some other vertical
% grasp. But, these usually give normals oriented towards the robot since
% the frontal face of the rim/object defines the normal.
%
% 2) Approach vector is almost, but not quite, vertical - just a bit of
% noise in the surface normal, as expected. Doesn't change the actual
% vector much, but makes it much more feasible to execute many grasps.

function ax = snapToVert(ax, ang)

VERT_THRESH = 0.85;

if (ang >= pi/4 && ang <= 3*pi/4) || abs(ax(3)) > VERT_THRESH
    ax = [0 0 sign(ax(3))]';
end