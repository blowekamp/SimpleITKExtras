import SimpleITK as sitk
import SimpleITK.utilities as sitkutils


def test_Logger():
    logger = sitkutils.Logger()


def test_make_isotropic():
    img = sitk.Image([10, 10, 5], sitk.sitkFloat32)
    img.SetSpacing([0.3, 0.3, 0.6])

    sitkutils.make_isotropic(img)


slice_call = 0


def test_slice_by_slice():
    @sitkutils.slice_by_slice
    def f(_img):
        global slice_call

        _img[:] = slice_call
        slice_call = 1 + slice_call
        return _img

    img = sitk.Image([10, 10, 5], sitk.sitkFloat32)
    img = f(img)

    for z in range(img.GetSize()[2]):
        assert img[0, 0, z] == z


def test_sitktovtk():
    img = sitk.Image([10, 10, 5], sitk.sitkFloat32)
    vtk_img = sitkutils.sitk2vtk(img)


def test_fft_initialization():
    fixed_img = sitk.Image([1024, 512], sitk.sitkInt8)

    fixed_img[510:520, 255:265] = 10

    moving_img = sitk.Image([1024, 512], sitk.sitkInt8)
    moving_img[425:435, 300:320] = 8

    tx = sitkutils.fft_based_translation_initialization(fixed_img, moving_img)
    assert tx.GetOffset() == (-85.0, 50.0)


def test_fft_initialization2():
    fixed_img = sitk.Image([1024, 512], sitk.sitkUInt8)

    fixed_img[510:520, 255:265] = 10

    moving_img = sitk.Image([1024, 512], sitk.sitkUInt8)
    moving_img.SetSpacing([1, 0.5])
    moving_img.SetOrigin([0, -0.25])
    moving_img[425:435, 305:315] = 8

    tx = sitkutils.fft_based_translation_initialization(fixed_img, moving_img)
    assert tx.GetOffset() == (-85.0, -105.0)
