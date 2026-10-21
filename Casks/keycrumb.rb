cask "keycrumb" do
  version "0.1.0-alpha.6"
  sha256 "8f5a3733fd686622d7e360e2ed90923c73be1f2d3f4f4c0cf2052680c61680e7"

  url "https://downloads.keycrumb.com/v#{version}/KeyCrumb-#{version}.dmg"
  name "KeyCrumb"
  desc "Menu bar reference viewer for local cheat sheets"
  homepage "https://keycrumb.com/"

  livecheck do
    url "https://downloads.keycrumb.com/appcast.xml"
    strategy :sparkle, &:short_version
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "KeyCrumb.app"

  uninstall quit: "com.keycrumb.app"
end
