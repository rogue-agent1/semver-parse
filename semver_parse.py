#!/usr/bin/env python3
"""SemVer parser and comparator from scratch."""
import sys,re
class SemVer:
    def __init__(self, s):
        m = re.match(r'^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+(.+))?$', s)
        if not m: raise ValueError(f"Invalid semver: {s}")
        self.major,self.minor,self.patch = int(m[1]),int(m[2]),int(m[3])
        self.pre = m[4]; self.build = m[5]
    def __repr__(self): return f"{self.major}.{self.minor}.{self.patch}" + (f"-{self.pre}" if self.pre else "")
    def _cmp_key(self):
        pre_key = (0, self.pre.split('.')) if self.pre else (1,)
        return (self.major, self.minor, self.patch, pre_key)
    def __lt__(self, o): return self._cmp_key() < o._cmp_key()
    def __eq__(self, o): return self._cmp_key() == o._cmp_key()
    def __le__(self, o): return self<o or self==o
    def bump(self, part):
        if part=="major": return SemVer(f"{self.major+1}.0.0")
        if part=="minor": return SemVer(f"{self.major}.{self.minor+1}.0")
        return SemVer(f"{self.major}.{self.minor}.{self.patch+1}")
def main():
    if "--demo" in sys.argv:
        versions = ["1.0.0","2.1.0","1.0.0-alpha","1.0.0-beta","0.9.9","2.0.0-rc.1","2.0.0"]
        parsed = [SemVer(v) for v in versions]
        print("Sorted:", " < ".join(str(v) for v in sorted(parsed)))
        v = SemVer("1.2.3")
        print(f"\n{v}.bump(major) = {v.bump('major')}")
        print(f"{v}.bump(minor) = {v.bump('minor')}")
        print(f"{v}.bump(patch) = {v.bump('patch')}")
    elif len(sys.argv)>1:
        v = SemVer(sys.argv[1])
        print(f"major={v.major} minor={v.minor} patch={v.patch} pre={v.pre}")
if __name__=="__main__": main()
