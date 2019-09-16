import bpy, bmesh
import glob

def loop_over_frames(fdir, blenderfile, 
                     isotype="obj", 
                     material_name='liquid',
                     smooth=False):

    """
        Run blender and loop through all files in
        directory fdir with file extension isotype,
        applies material liquid and save to image 
        files.

        Note requires to be run in blender or define an alias like
        blenpy /path/to//blender --background --python
    """

    #Load blender file
    bpy.ops.wm.open_mainfile(filepath=fdir+blenderfile)
    iso_files = glob.glob(fdir+"/*."+isotype)

    for f in iso_files:

        #Import new object
        bpy.ops.import_scene.obj(filepath=fdir+"/"+iso_files)
        obj = bpy.context.selected_objects[:][0]

        #Set material to choice
        mat = bpy.data.materials[material_name]
        obj.data.materials[0] = mat

        #Smooth
        if smooth:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            mesh=bmesh.from_edit_mesh(obj.data)
            for v in mesh.verts:
                v.select = True
            bpy.context.scene.objects.active = bpy.context.scene.objects.active
            bpy.ops.mesh.vertices_smooth(repeat=5)


        #Render to file
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.data.scenes['Scene'].render.filepath = fdir+'./image{:05d}'.format(i)+'.jpg'
        bpy.ops.render.render( write_still=True )

        #Delete old wave object
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = obj
        obj.select = True
        bpy.ops.object.delete()


