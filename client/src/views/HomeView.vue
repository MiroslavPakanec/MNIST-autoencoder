<template>
  <div id="container" >
    <div id="navbar" :style="{'width': `${canvasWidth}px`, 'marginTop': `${marginTop}px`}">
      <button class="btn btn-loader" @click="loadImage()" :disabled="isProcessing">Load new image</button>
      <button class="btn" @click="copy()" :disabled="isProcessing || !imageStore.isWatermarkingReady">{{ copyButtonText }}</button>
      <button class="btn btn-loader" @click="predictImage()" :disabled="pixelStore.masks.length === 0 || modelId.length === 0">Predict</button>
      <button class="btn btn-loader" @click="imageStore.reset()" :disabled="isProcessing">Reset</button>
    </div>
    <div id="canvas-container" :style="{ 'height': `${canvasHeight}px`}">
      <div id="watermark-container" :style="{ 'height': `${canvasHeight}px`}" >
        <span class="container-title">Watermarks</span>
        <button class="btn" v-for="(watermark, index) in imageStore.watermarks" :key="index" :class="{'active': imageStore.isWatermarkActive(index)}" :disabled="!imageStore.isWatermarkingReady" @click="imageStore.setWatermark(index)">{{watermark.w}} x {{watermark.h}}</button>
        <span id="watermark-counter">{{ pixelStore.masks.length }} / {{ pixelStore.maxMasks }}</span>
        <button class="btn" :disabled="!imageStore.isWatermarkingReady || pixelStore.masks.length === 0" @click="imageStore.resetWatermarks()">Clear</button>
        <button class="btn" :disabled="!imageStore.isWatermarkingReady || pixelStore.masks.length === 0" @click="showWatermarks = !showWatermarks">{{showWatermarksText}}</button>
      </div>
      <div>
        <div id="canvas" :style="{ 'height': `${canvasHeight}px`, 'width': `${canvasWidth}px` }" />
        <span id=version>Model: {{ modelId }}</span>
      </div>
      <div id="image-type-container" :style="{ 'height': `${canvasHeight}px`}" >
        <span class="container-title">Image type</span>
        <button class="btn" @click="imageStore.setActiveImage('original')" :class="{'active': imageStore.activeImage === 'original'}" :disabled="!showOriginal">Original</button>
        <button class="btn" @click="imageStore.setActiveImage('watermarked')" :class="{'active': imageStore.activeImage === 'watermarked'}" :disabled="!showWatermarked">Watermarked</button>
        <button class="btn" @click="imageStore.setActiveImage('reconstructed')" :class="{'active': imageStore.activeImage === 'reconstructed'}" :disabled="!showReconstructed">Reconstructed</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import p5 from 'p5'
import { ComputedRef, Ref, computed, onMounted, ref } from 'vue'
import { usePixelStore } from '@/stores/pixelStore'
import { ImagePayload, PredictedImagePayload, WatermarkPayload, useHttpStore } from '@/stores/httpStore'
import { useColorStore } from '@/stores/colorStore';
import { Watermark, useImageStore } from '@/stores/imageStore';

const pixelStore = usePixelStore()
const httpStore = useHttpStore()
const colorStore = useColorStore()
const imageStore = useImageStore()

const primary: string = colorStore.primary
const secondary: string = colorStore.secondary
const ternary: string = colorStore.ternary
const borderPrimary = `1px solid ${primary}`
const borderTernary = `1px solid ${ternary}`

const modelId: string = process.env.VUE_APP_EXPERIMENT_ID.length === 0 ? '[not set]' : process.env.VUE_APP_EXPERIMENT_ID

const showWatermarks: Ref<boolean> = ref(false)
const showWatermarksText: ComputedRef<string> = computed(() => showWatermarks.value ? 'Hide' : 'Show')
const copyButtonText: Ref<string> = ref('Copy')
  
const showOriginal: ComputedRef<boolean> = computed(() => imageStore.isWatermarkingReady)
const showWatermarked: ComputedRef<boolean> = computed(() => imageStore.isWatermarkingReady && pixelStore.masks.length > 0)
const showReconstructed: ComputedRef<boolean> = computed(() => imageStore.hasReconstructedImage)

const canvasPercent: Ref<number> = ref(0.6)
const canvasWidth: Ref<number> = ref(window.innerHeight * canvasPercent.value)
const canvasHeight: Ref<number> = ref(window.innerHeight * canvasPercent.value)
const marginTop: ComputedRef<number> = computed(() => (window.innerHeight / 2) - (canvasHeight.value / 2))
const isProcessing: ComputedRef<boolean> = computed(() => httpStore.isFetching || pixelStore.isProcessing)
const mouseXPercent: Ref<number> = ref(0)
const mouseYPercent: Ref<number> = ref(0)

const isCanvasHover: ComputedRef<boolean> = computed(() => mouseXPercent.value > 0 && mouseXPercent.value < 100 && mouseYPercent.value > 0 && mouseYPercent.value < 100)
const watermarkPixelX: ComputedRef<number | undefined> = computed(() => isCanvasHover.value ? Math.floor(28 * (mouseXPercent.value / 100)) : undefined)
const watermarkPixelY: ComputedRef<number | undefined> = computed(() => isCanvasHover.value ? Math.floor(28 * (mouseYPercent.value / 100)) : undefined)
const watermarkStartX: ComputedRef<number | undefined>  = computed(() => watermarkPixelX.value !== undefined ? watermarkPixelX.value - (Math.ceil(imageStore.getWatermark().w / 2) - 1) : undefined)
const watermarkEndX: ComputedRef<number | undefined> = computed(() => watermarkPixelX.value !== undefined ? watermarkPixelX.value + (Math.ceil(imageStore.getWatermark().w / 2)) : undefined)
const watermarkStartY: ComputedRef<number | undefined> = computed(() => watermarkPixelY.value !== undefined ? watermarkPixelY.value - (Math.ceil(imageStore.getWatermark().h / 2) - 1) : undefined)
const watermarkEndY: ComputedRef<number | undefined> = computed(() => watermarkPixelY.value !== undefined ? watermarkPixelY.value + (Math.ceil(imageStore.getWatermark().h / 2)) : undefined)


const drawPixels = (sketch: any): void => {
  sketch.stroke(150, 150, 150)
  sketch.strokeWeight = 1

  const isWatermarkingReady: boolean = watermarkStartX.value !== undefined && watermarkEndX.value !== undefined && watermarkStartY.value !== undefined && watermarkEndY.value !== undefined && imageStore.isWatermarkingReady
  const pixels: number[][] = pixelStore.getPixels()

  for (let i = 0; i < pixels.length; i++) {
    const row = pixels[i]
    for (let j = 0; j < row.length; j++) {
      const pixel: number = row[j]
      
      sketch.fill(pixel, pixel, pixel)
      const drawWatermark = isWatermarkingReady && i >= watermarkStartX.value! && i <= watermarkEndX.value! && j >= watermarkStartY.value! && j <= watermarkEndY.value!
      if (drawWatermark) sketch.fill(36, 7, 80)

      const w: number = canvasWidth.value / 28
      const h: number = w
      const x: number = (w * i) - (canvasHeight.value / 2)
      const y: number = (h * j) - (canvasHeight.value / 2)
      sketch.rect(x, y, w, h)
    }
  }
}

const drawMasks = (sketch: any): void => {
  sketch.stroke(36, 7, 80)
  sketch.fill(169, 142, 209)
  const w: number = canvasWidth.value / 28
  const h: number = w

  for (const mask of pixelStore.masks) {
    for (let i = mask.sx; i <= mask.ex; i++) {
      for (let j = mask.sy; j <= mask.ey; j++) {
        const x: number = (w * i) - (canvasHeight.value / 2)
        const y: number = (h * j) - (canvasHeight.value / 2)
        sketch.rect(x, y, w, h)
      }
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
    if (showWatermarks.value) drawMasks(sketch)
  }

  sketch.mouseMoved = () => {
    mouseXPercent.value = clamp(0, sketch.mouseX / canvasWidth.value, 1) * 100
    mouseYPercent.value = clamp(0, sketch.mouseY / canvasHeight.value, 1) * 100
  }

  sketch.mousePressed = () => {
    if (sketch.mouseButton === sketch.LEFT && isCanvasHover.value && imageStore.isWatermarkingReady) imageStore.addWatermark(watermarkStartX.value, watermarkEndX.value, watermarkStartY.value, watermarkEndY.value) 
  }
}

const clamp = (value: number, min: number, max: number): number => Math.min(Math.max(value, min), max)

const copy = async (): Promise<void> => {
  const pixels: number[] = pixelStore.getFlatPixels()
  const pixelStr: string = JSON.stringify(pixels)
  await navigator.clipboard.writeText(pixelStr)
  copyButtonText.value = 'Copied!'
  setTimeout(() => {
    copyButtonText.value = 'Copy';
  }, 2000);
}


const loadImage = async (): Promise<void> => {
  const payload: ImagePayload | undefined = await httpStore.loadImages()
  if (!payload || !payload.y) return
  imageStore.setWithNewImage(payload.y)
}

const predictImage = async (): Promise<void> => {
  const pixels: number[] = pixelStore.getFlatPixels()
  const payload: PredictedImagePayload | undefined = await httpStore.predictImage(pixels)
  if (!payload || !payload.y) return
  imageStore.setReconstructedImage(payload.y)
  showWatermarks.value = false
}

const loadWatermarks = async (): Promise<void> => {
  const payload: WatermarkPayload | undefined = await httpStore.loadWatermarks()
  if (!payload || payload.length === 0) return
  const watermarks: Watermark[] = payload.map((x: [number, number]) => { return { w: x[0], h: x[1] }})
  imageStore.setWatermarks(watermarks)
}

onMounted(async () => {
  const sketch_element = document.getElementById('canvas')
  if (sketch_element === null) return
  new p5(sketch, sketch_element)
  await loadWatermarks()
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

#image-type-container {
  width: 200px;
  display: flex;
  flex-direction: column;
  align-items: flex;
  justify-content: flex-start;
  gap: 10px;
}

.container-title {
  padding-bottom: 10px;
}

#watermark-counter {
  padding-top: 50px;
  padding-bottom: 50px;
}

#canvas {
  padding: 10px;
  background-color: white;
  border-radius: 20px;
  box-sizing: content-box;
  cursor: none;
}

#navbar {
  margin: auto;
  margin-bottom: 30px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 5px;
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
  border: v-bind(borderPrimary);
  color: v-bind(primary);
  background-color: v-bind(secondary);
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

#version {
  padding-top: 5px;
  float: left;
  color: v-bind(ternary);
}
</style>
