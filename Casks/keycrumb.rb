cask "keycrumb" do
  version "0.2.0"
  sha256 "15fd7e2101987133d28af1010db9fba05af02b0c81b1b6e96a5d4bc1b5163562"

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
  depends_on macos: :tahoe

  app "KeyCrumb.app"

  uninstall quit: "com.keycrumb.app"
end
