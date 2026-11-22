package Updater with SPARK_Mode => On is

   --  A release is only publishable when every advertised platform has an asset.
   --  Missing macOS assets were the real failure mode for old GNAT Studio
   --  releases, so those are named fields rather than a single Boolean.
   type Asset_Set is record
      Linux_X86_64  : Boolean;
      Linux_AArch64 : Boolean;
      Macos_X86_64  : Boolean;
      Macos_AArch64 : Boolean;
   end record;

   type Blocker is
     (None, No_New_Version, Bad_Token, Missing_Linux_X86_64,
      Missing_Linux_AArch64, Missing_Macos_X86_64, Missing_Macos_AArch64);

   function All_Assets (A : Asset_Set) return Boolean is
     (A.Linux_X86_64 and then A.Linux_AArch64 and then
      A.Macos_X86_64 and then A.Macos_AArch64);

   function Ready (Newer, Token_OK : Boolean; A : Asset_Set) return Boolean is
     (Newer and then Token_OK and then All_Assets (A));

   function First_Blocker
     (Newer : Boolean; Token_OK : Boolean; A : Asset_Set) return Blocker
   with Post =>
     (case First_Blocker'Result is
        when None     => Ready (Newer, Token_OK, A),
        when others   => not Ready (Newer, Token_OK, A));

end Updater;
