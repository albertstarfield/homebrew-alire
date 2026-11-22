class Alr < Formula
  desc "Ada and SPARK package manager"
  homepage "https://alire.ada.dev/"
  version "2.1.1"

  on_macos do
    on_arm do
      url "https://github.com/alire-project/alire/releases/download/v2.1.1/alr-2.1.1-bin-aarch64-macos.zip"
      sha256 "2c4867bfff3b95ecd9d846df460a52983d2b0072808b341f8fa5d82494fb309e"
    end
    on_intel do
      url "https://github.com/alire-project/alire/releases/download/v2.1.1/alr-2.1.1-bin-x86_64-macos.zip"
      sha256 "d3e16cdfaf0cfb2da62853b79b62910189fdca9d5fddc5c3ac5974ffc7d9544b"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/alire-project/alire/releases/download/v2.1.1/alr-2.1.1-bin-aarch64-linux.zip"
      sha256 "d76c93ad3dc631826144e10bdabc6b3bf98783805bebfd5e4a0e852dd524d812"
    end
    on_intel do
      url "https://github.com/alire-project/alire/releases/download/v2.1.1/alr-2.1.1-bin-x86_64-linux.zip"
      sha256 "09c66bcd8c35dd4b97b72c3d9b76e44caa6964a2db35aba069f396f00f1f64c7"
    end
  end

  def install
    bin.install "bin/alr"
  end

  test do
    assert_match "alr", shell_output("#{bin}/alr --version")
  end
end
