import omni.ext
import omni.ui as ui
import omni.usd
import omni.kit.commands
import omni.kit.browser.asset
from random import randrange
from pxr import Sdf, Gf, Usd, UsdGeom

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    treenum=0
    howmany = 10
    density = 0
    spawntype = 0
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[jason.spawn.cube] MyExtension startup")
        self._window = ui.Window("Landscape Generator", width=300, height=300)
        with self._window.frame:
            with ui.VStack():

                treeselect = ui.ComboBox(0, "Australian Tree Fern", "Cuban Royal Palm", "Japanese Fiber Banana", height = 20)
                ui.Label("Select Number of Trees",alignment=ui.Alignment.CENTER, height=20)
                numtreeslider = ui.IntSlider(min=1,max=50, height=20)
                ui.Label("Select Density",alignment=ui.Alignment.CENTER, height=20)
                densityslider = ui.FloatSlider(min=0,max=.99, height=20)
                ui.Button("Spawn World", clicked_fn=lambda: spawnworld(), height=50)
                ui.Button("Delete all Objects", clicked_fn=lambda: deleteall(),height=10)

        def setselectiontype(num):
            if num == 0:
                MyExtension.selectiontype=0
            else:
                MyExtension.selectiontype=1

        def spawnworld():
            deleteall()
            addHDRIandsun()
            addPlane()
            if MyExtension.spawntype==0:
                spawnTrees()
            else:
                spawnobject()

            context=omni.usd.get_context()
            stage = context.get_stage()
              
        def addHDRIandsun():
                omni.kit.commands.execute('CreateHdriSkyCommand',
                    sky_url='http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Skies/Clear/noon_grass_4k.hdr',
                    sky_path='/Environment/sky')
                omni.kit.commands.execute('CreatePrim',
                    prim_type='DistantLight',
                    attributes={'angle': 1.0, 'intensity': 3000})

        def addPlane():
            omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
                prim_type='Plane')

            omni.kit.commands.execute('CreateMdlMaterialPrimCommand',
                mtl_url='http://omniverse-content-production.s3-us-west-2.amazonaws.com/Materials/Base/Natural/Grass_Cut.mdl',
                mtl_name='Grass_Cut',
                mtl_path='/World/Looks/Grass_Cut')

            omni.kit.commands.execute('BindMaterialCommand',
                prim_path='/Plane',
                material_path='/World/Looks/Grass_Cut',
                strength='strongerThanDescendants')

            omni.kit.commands.execute('BindMaterialCommand',
                prim_path='/Plane',
                material_path='/World/Looks/Grass_Cut',
                strength='strongerThanDescendants')


            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/Plane.xformOp:scale'),
                value=Gf.Vec3d(40.0, 1.0, 40.0),
                prev=Gf.Vec3d(40.0, 1.0, 1.0))

        def spawnTrees():
                MyExtension.treenum=treeselect.model.get_item_value_model().get_value_as_int()
                MyExtension.howmany = numtreeslider.model.get_value_as_int()
                MyExtension.density = densityslider.model.get_value_as_float()
                if(MyExtension.treenum==0):
                    for i in range(MyExtension.howmany):
                        omni.kit.commands.execute('CreateReferenceCommand',
                        asset_path="http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Vegetation/Plant_Tropical/Australian_Tree_Fern.usd",
                        path_to = '/World/Australian_Tree_Fern',
                        usd_context = omni.usd.get_context())
                        omni.kit.commands.execute('TransformPrimSRT',
                            path=Sdf.Path('/World/Australian_Tree_Fern'+createending(i)),
                            new_translation=Gf.Vec3d(calcdensity(MyExtension.density), 0, calcdensity(MyExtension.density)),
                            new_rotation_euler=Gf.Vec3f(0.0, -90.0, -90.0),
                            new_rotation_order=Gf.Vec3i(0, 1, 2),
                            new_scale=Gf.Vec3f(5, 5, 5),
                            old_translation=Gf.Vec3d(0.0, 0.0, 0.0),
                            old_rotation_euler=Gf.Vec3f(0.0, -90.0, -90.0),
                            old_rotation_order=Gf.Vec3i(0, 1, 2),
                            old_scale=Gf.Vec3f(1.0, 1.0, 1.0))
                elif(MyExtension.treenum==1):
                    for i in range(MyExtension.howmany):
                        omni.kit.commands.execute('CreateReferenceCommand',
                        asset_path="http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Vegetation/Plant_Tropical/Cuban_Royal_Palm.usd",
                        path_to = '/World/Cuban_Royal_Palm',
                        usd_context = omni.usd.get_context())
                        omni.kit.commands.execute('TransformPrimSRT',
                            path=Sdf.Path('/World/Cuban_Royal_Palm'+createending(i)),
                            new_translation=Gf.Vec3d(calcdensity(MyExtension.density), 0, calcdensity(MyExtension.density)),
                            new_rotation_euler=Gf.Vec3f(0.0, -90.0, -90.0),
                            new_rotation_order=Gf.Vec3i(0, 1, 2),
                            new_scale=Gf.Vec3f(5, 5, 5),
                            old_translation=Gf.Vec3d(0.0, 0.0, 0.0),
                            old_rotation_euler=Gf.Vec3f(0.0, -90.0, -90.0),
                            old_rotation_order=Gf.Vec3i(0, 1, 2),
                            old_scale=Gf.Vec3f(1.0, 1.0, 1.0))
                elif(MyExtension.treenum==2):
                    for i in range(MyExtension.howmany):
                            omni.kit.commands.execute('CreateReferenceCommand',
                            asset_path="http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Vegetation/Plant_Tropical/Japanese_Fiber_Banana.usd",
                            path_to = '/World/Japanese_Fiber_Banana',
                            usd_context = omni.usd.get_context())
                            omni.kit.commands.execute('TransformPrimSRT',
                                path=Sdf.Path('/World/Japanese_Fiber_Banana'+createending(i)),
                                new_translation=Gf.Vec3d(calcdensity(MyExtension.density), 0, calcdensity(MyExtension.density)),
                                new_rotation_euler=Gf.Vec3f(0.0, -90.0, -90.0),
                                new_rotation_order=Gf.Vec3i(0, 1, 2),
                                new_scale=Gf.Vec3f(5, 5, 5),
                                old_translation=Gf.Vec3d(0.0, 0.0, 0.0),
                                old_rotation_euler=Gf.Vec3f(0.0, -90.0, -90.0),
                                old_rotation_order=Gf.Vec3i(0, 1, 2),
                                old_scale=Gf.Vec3f(1.0, 1.0, 1.0))

        def spawnobject():
            MyExtension.howmany = numtreeslider.model.get_value_as_int()
            MyExtension.density = densityslider.model.get_value_as_float()
            context=omni.usd.get_context()
            stage = context.get_stage()
            prims = [stage.GetPrimAtPath(m) for m in context.get_selection().get_selected_prim_paths()]
            for p in prims:
                for i in range(MyExtension.howmany):
                            omni.kit.commands.execute('CreateReferenceCommand',
                            asset_path=p,
                            path_to = '/World/Object',
                            usd_context = omni.usd.get_context())
                            omni.kit.commands.execute('TransformPrimSRT',
                                path=Sdf.Path('/World/Object'+createending(i)),
                                new_translation=Gf.Vec3d(calcdensity(MyExtension.density), 0, calcdensity(MyExtension.density)),
                                new_rotation_euler=Gf.Vec3f(0.0, -90.0, -90.0),
                                new_rotation_order=Gf.Vec3i(0, 1, 2),
                                new_scale=Gf.Vec3f(5, 5, 5),
                                old_translation=Gf.Vec3d(0.0, 0.0, 0.0),
                                old_rotation_euler=Gf.Vec3f(0.0, -90.0, -90.0),
                                old_rotation_order=Gf.Vec3i(0, 1, 2),
                                old_scale=Gf.Vec3f(1.0, 1.0, 1.0))

        def calcdensity(density):
            return randrange(int(-2000*(density*-1+1)),int(2000*(density*-1+1)))

        def createending(num):
            if num==0:
                return ""
            elif num < 10:
                return "_0" + str(num)
            else:
                return "_" + str(num)

        def deleteall():
            context=omni.usd.get_context()
            stage = context.get_stage()
            omni.kit.commands.execute('SelectAll')
            prims = [stage.GetPrimAtPath(m) for m in context.get_selection().get_selected_prim_paths()]
            for p in range(len(prims)):
                prims[p] = str(prims[p])
                prims[p] = prims[p][prims[p].index("/"):prims[p].index('>')]
            omni.kit.commands.execute('DeletePrims',paths=prims)

    def on_shutdown(self):
        print("[jason.spawn.cube] MyExtension shutdown")
