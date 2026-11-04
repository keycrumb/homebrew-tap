cask "keycrumb" do
  version "0.1.0-alpha.14"
  sha256 "d1744e8b7ebf95b05b6200df1b7ff5139d50c12be0c124383d584da0ceef7f8f"

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
