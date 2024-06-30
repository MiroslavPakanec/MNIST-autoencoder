<template>
  <div id="container" >
    <div id="navbar" :style="{'width': `${canvasWidth}px`, 'marginTop': `${marginTop}px`}">
      <button class="btn btn-loader" @click="loadImage()" :disabled="isGenerateButtonDisabled">Load new image</button>
      <button class="btn btn-loader" :disabled="true">Predict</button>
      <button class="btn btn-loader" @click="imageStore.reset()" :disabled="isGenerateButtonDisabled">Reset</button>
    </div>
    <div id="canvas-container" :style="{ 'height': `${canvasHeight}px`}">
      <div id="watermark-container" :style="{ 'height': `${canvasHeight}px`}" >
        <span id="watermark-title">Watermarks</span>
        <button class="btn" v-for="(watermark, index) in imageStore.watermarks" :key="index" :class="{'active': imageStore.isWatermarkActive(index)}" :disabled="!imageStore.isWatermarkingReady" @click="imageStore.setWatermark(index)">{{watermark.w}} x {{watermark.h}}</button>
      </div>
      <div id="canvas" :style="{ 'height': `${canvasHeight}px`, 'width': `${canvasWidth}px` }" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import p5 from 'p5'
import { ComputedRef, Ref, computed, onMounted, ref } from 'vue'
import { usePixelStore } from '@/stores/pixelStore'
import { ImagePayload, useHttpStore } from '@/stores/httpStore'
import { useColorStore } from '@/stores/colorStore';
import { useImageStore } from '@/stores/imageStore';
import SelectButton from 'primevue/selectbutton';

const pixelStore = usePixelStore()
const httpStore = useHttpStore()
const colorStore = useColorStore()
const imageStore = useImageStore()

const canvasPercent: Ref<number> = ref(0.6)
const canvasWidth: Ref<number> = ref(window.innerHeight * canvasPercent.value)
const canvasHeight: Ref<number> = ref(window.innerHeight * canvasPercent.value)
const marginTop: ComputedRef<number> = computed(() => (window.innerHeight / 2) - (canvasHeight.value / 2))
const isGenerateButtonDisabled: ComputedRef<boolean> = computed(() => httpStore.isFetching || pixelStore.isProcessing)
const mouseXPercent: Ref<number> = ref(0)
const mouseYPercent: Ref<number> = ref(0)

const primary: string = colorStore.primary
const secondary: string = colorStore.secondary
const ternary: string = colorStore.ternary
const borderTernary = `1px solid ${ternary}`

const drawPixels = (sketch: any): void => {
  sketch.stroke(150, 150, 150)
  sketch.strokeWeight = 1
  for (let i = 0; i < pixelStore.pixels.length; i++) {
    const row = pixelStore.pixels[i]
    for (let j = 0; j < row.length; j++) {
      const pixel: number = row[j]
      sketch.fill(pixel, pixel, pixel)
      const w: number = canvasWidth.value / 28
      const h: number = w
      const x: number = (w * i) - (canvasHeight.value / 2)
      const y: number = (h * j) - (canvasHeight.value / 2)
      sketch.rect(x, y, w, h)
    }
  }
}

const sketch = (sketch: any) => {
  sketch.setup = () => {
    sketch.createCanvas(canvasWidth.value, canvasHeight.value, sketch.WEBGL)
    pixelStore.reset()
  }

  sketch.windowResized = () => {
    canvasWidth.value = window.innerHeight * canvasPercent.value
    canvasHeight.value = window.innerHeight * canvasPercent.value
  }

  sketch.draw = () => {
    sketch.background(255,255,255)
    drawPixels(sketch)
  }

  sketch.mouseMoved = () => {
    mouseXPercent.value = clamp(0, sketch.mouseX / canvasWidth.value, 1) * 100
    mouseYPercent.value = clamp(0, sketch.mouseY / canvasHeight.value, 1) * 100
  }
}

const clamp = (value: number, min: number, max: number): number => Math.min(Math.max(value, min), max)

const loadImage = async (): Promise<void> => {
  const payload: ImagePayload | undefined = await httpStore.loadImages()
  if (!payload || !payload.y) return
  imageStore.setWithNewImage(payload.y)
}

onMounted(() => {
  const sketch_element = document.getElementById('canvas')
  if (sketch_element === null) return
  new p5(sketch, sketch_element)
})
</script>

<style scoped>
span {
  color: white;
}


#container {
  height: 100vh;
  width: 100vw;
  overflow-x: hidden;
  background: v-bind(secondary);
}

#canvas-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin: auto;
  gap: 20px;
}

#watermark-container {
  width: 100px;
  display: flex;
  flex-direction: column;
  align-items: flex;
  justify-content: flex-start;
  gap: 10px;
}

#watermark-title {
  padding-bottom: 10px;
}

#canvas {
  padding: 10px;
  background-color: white;
  border-radius: 20px;
  box-sizing: content-box;
}

#navbar {
  margin: auto;
  margin-bottom: 30px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 5px;
  padding-left: 60px;
  gap: 10px;
}

.btn {
  padding: 15px;
  border: v-bind(borderTernary);
  background-color: transparent;
  color: v-bind(ternary);
  border-radius: 5px;
  height: 50px;
}

.btn-loader {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.btn:hover, .btn.active {
  cursor: pointer;
  border: 1px solid white;
  color: #872341;
  background-color: white;
}

.btn:disabled {
  border: 1px solid #4e2c5b;
  color: #4e2c5b;
  background-color: rgba(183, 0, 255, 0.2);
  cursor: not-allowed;
}

.loader {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: inline-block;
  border-top: 1px solid white;
  border-right: 1px solid transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}
.loader::after {
  content: '';  
  box-sizing: border-box;
  position: absolute;
  left: 0;
  top: 0;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border-bottom: 1px solid #4e2c5b;
  border-left: 1px solid transparent;
}
@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
} 


</style>
