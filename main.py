import asyncio
import pathlib
import shutil
import zipfile

from pymobiledevice3.exceptions import (
    AlreadyMountedError,
    ConnectionFailedError,
    FatalPairingError,
    IncorrectModeError,
    NoDeviceConnectedError,
    PyMobileDevice3Exception,
)
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.installation_proxy import InstallationProxyService
from pymobiledevice3.services.mobile_image_mounter import MobileImageMounterService
import httpx


DEVELOPER_IOS_IMAGES_PATH = "./xcode_developer_images"


async def download_ios_developer_image(lockdown_client: LockdownClient) -> None:
    file_name = f"{lockdown_client.ios_version[:4]}.zip"
    folder = pathlib.Path(
        f"{DEVELOPER_IOS_IMAGES_PATH}/{lockdown_client.ios_version[:4]}"
    )
    if folder.exists() is False:
        url = f"https://github.com/mspvirajpatel/Xcode_Developer_Disk_Images/releases/download/{lockdown_client.ios_version[:4]}/{file_name}"
        async with httpx.AsyncClient() as ac:
            response = await ac.get(url, follow_redirects=True)
            with open(f"{DEVELOPER_IOS_IMAGES_PATH}/{file_name}", "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

            z = zipfile.ZipFile(f"{DEVELOPER_IOS_IMAGES_PATH}/{file_name}", "r")
            z.extractall(path=f"{DEVELOPER_IOS_IMAGES_PATH}")
            pathlib.Path(f"{DEVELOPER_IOS_IMAGES_PATH}/{file_name}").unlink()

            folder = pathlib.Path("__MACOSX")
            if folder.exists() is True:
                shutil.rmtree("__MACOSX")


def mount_developer_image(lockdown_client: LockdownClient) -> None:
    mounter = MobileImageMounterService(lockdown_client)

    image_path = (
        pathlib.Path(DEVELOPER_IOS_IMAGES_PATH)
        / mounter.lockdown.sanitized_ios_version
        / "DeveloperDiskImage.dmg"
    )
    if pathlib.Path(image_path).exists() is False:
        raise RuntimeError(f"File {image_path} not found.")

    signature = image_path.with_suffix(".dmg.signature").read_bytes()
    try:
        mounter.upload_image("Developer", image_path.read_bytes(), signature)
    except (
        ConnectionAbortedError,
        BrokenPipeError,
        PyMobileDevice3Exception,
    ) as e:
        raise RuntimeError(repr(e))
    try:
        mounter.mount("Developer", signature)
    except AlreadyMountedError as e:
        raise RuntimeError(repr(e))


async def install_sber(ios_serial: str, ipa_path: str) -> None:
    if pathlib.Path(ipa_path).exists is False:
        pass
        raise FileNotFoundError

    try:
        lockdown_client = LockdownClient(ios_serial)
    except (
        ConnectionFailedError,
        ConnectionRefusedError,
        FatalPairingError,
        NoDeviceConnectedError,
        IncorrectModeError,
        PyMobileDevice3Exception,
    ) as e:
        raise RuntimeError(repr(e))

    await download_ios_developer_image(lockdown_client)
    try:
        mount_developer_image(lockdown_client)
    except (ConnectionRefusedError, ConnectionFailedError, OSError) as e:
        raise RuntimeError(repr(e))

    InstallationProxyService(lockdown=lockdown_client).install_from_local(ipa_path)


async def main() -> None:
    ios_serial = ""
    ipa_path = "./ios-apps/sberbank.ipa"
    try:
        await install_sber(ios_serial, ipa_path)
    except FileNotFoundError:
        print(f"File {ipa_path} not found.\nApp is not installed.")
    except RuntimeError as e:
        print(
            f"Error in connect to device '{ios_serial}'. Check usbmuxd running.\nDetail: {repr(e)}."
        )


if __name__ == "__main__":
    asyncio.run(main())
