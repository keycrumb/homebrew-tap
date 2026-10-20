cask "keycrumb" do
  version "0.1.0-alpha.4"
  sha256 "fb99524facb7e05c383b1414f900295ecf4d7f5e441ef6c6284771ef5cb1227b"

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
