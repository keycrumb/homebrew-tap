cask "keycrumb" do
  version "0.1.0-alpha.12"
  sha256 "3beadf9c3a9da4b18b7ab5978634f6045d305b0ecd05086682b223c262747ab7"

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
