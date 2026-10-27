cask "keycrumb" do
  version "0.1.0-alpha.10"
  sha256 "b7af8adf12ec667f44ad7b7a9c696dd09402cd605792ce656e888750d8e881ec"

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
