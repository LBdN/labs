      #elf.accept('escape', sys.exit)
      #self.accept('+', self.ZoomIn)
      #self.accept('+-repeat', self.ZoomIn)
      #self.accept('-', self.ZoomOut)
      #self.accept('--repeat', self.ZoomOut)
      #self.accept('*', self.RotateCW)
      #self.accept('*-repeat', self.RotateCW)
      #self.accept('/', self.RotateCCW)
      #self.accept('/-repeat', self.RotateCCW)
      #self.accept('enter', self.Cycle)
      #self.accept('0', self.ResetPos)
      #self.accept('5', self.RotateZ)
      
      #self.seq = 0
      
      ##this doesn't work after embedding panda into pyqt, so it's commented
      ##self.ResetPos()
      
   #def ResetPos(self):
      #if self.seq <> 0 and self.seq.isPlaying(): return
      #base.disableMouse()
      #base.camera.setPos(0,-15,0)
      #base.camera.setHpr(0,0,0)
      #self.cycle = -2
      #self.Cycle()

   #def move(self, lerp) :
      #if self.seq <> 0 and self.seq.isPlaying(): 
          #return
      #self.seq = Sequence(lerp)
      #self.seq.start()

   #def ZoomIn(self):
      #posLerp = LerpPosInterval(base.camera,0.3,VBase3(0,base.camera.getY()+1,0),blendType='easeInOut')
      #self.move(posLerp)
      
   #def ZoomOut(self):
      #posLerp = LerpPosInterval(base.camera,0.3,VBase3(0,base.camera.getY()-1,0),blendType='easeInOut')
      #self.move(posLerp)
      
   #def RotateCW(self):
      #hprLerp = LerpHprInterval(base.camera,0.6,VBase3(0,0,base.camera.getR()-45),blendType='easeInOut')
      #self.move(hprLerp)
      
   #def RotateZ(self):
      #hprLerp = LerpHprInterval(self.data.nodePath,2,VBase3(self.data.nodePath.getH()+360,0,0),blendType='easeInOut')
      #self.move(hprLerp)
      
   #def RotateCCW(self):
      #hprLerp = LerpHprInterval(base.camera,0.6,VBase3(0,0,base.camera.getR()+45),blendType='easeInOut')
      #self.move(hprLerp)

   #def Cycle(self):
      #self.cycle = self.cycle + 1
      #if self.cycle == len(self.data.graphs): self.cycle = -1
      #for idx, i in enumerate(self.data.graphs):
         #if self.cycle == -1 or self.cycle == idx:
            #i.nodePathGraphLab.show()
         #else:
            #i.nodePathGraphLab.hide()
 
