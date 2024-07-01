import { defineStore } from "pinia"
import { ComputedRef, Ref, computed, ref } from "vue"
import { Mask, usePixelStore } from "./pixelStore"

export type Watermark = { w: number, h: number }
export type ImageState = 'none' | 'original' | 'watermarked' | 'reconstructed'

export const useImageStore = defineStore('image', () => {
    const pixelStore = usePixelStore()

    const originalImage: Ref<number[] | undefined> = ref(undefined)
    const watermarkedImage: Ref<number[] | undefined> = ref(undefined)
    const recostructedImage: Ref<number[] | undefined> = ref(undefined)

    const activeImage: Ref<ImageState> = ref('none')

    const setActiveImage = (state: ImageState): void => {
        if (state === 'original') pixelStore.setPixels(originalImage.value!)
        if (state === 'watermarked') pixelStore.setPixels(watermarkedImage.value!)
        if (state === 'reconstructed') pixelStore.setPixels(recostructedImage.value!)
        activeImage.value = state
    }

    const setWithNewImage = (image: number[]): void => {
        originalImage.value = image
        watermarkedImage.value = image
        recostructedImage.value = undefined

        activeImage.value = 'original'
        pixelStore.setPixels(image)
    }

    const setReconstructedImage = (image: number[]): void => {
        recostructedImage.value = image
        activeImage.value = 'reconstructed'
        pixelStore.setPixels(image)
    }

    const reset = (): void => {
        originalImage.value = undefined
        watermarkedImage.value = undefined
        recostructedImage.value = undefined
        activeImage.value = 'none'
        pixelStore.reset()
    }

    const isWatermarkingReady: ComputedRef<boolean> = computed(() => originalImage.value !== undefined && watermarkedImage.value !== undefined)

    const watermarks: Ref<Watermark[]> = ref([
        { w: 2, h: 12 },
        { w: 12, h: 2 },
        { w: 8, h: 4 },
        { w: 4, h: 8 },
    ])

    const activeWatermarkIndex: Ref<number> = ref(0)
    const getWatermark = (): Watermark => watermarks.value[activeWatermarkIndex.value]
    const setWatermark = (index: number) => activeWatermarkIndex.value = index
    const isWatermarkActive = (index: number) => activeWatermarkIndex.value === index

    const addWatermark = (startX: number | undefined, endX: number | undefined, startY: number | undefined, endY: number | undefined): void => {
        if (startX === undefined || endX === undefined || startY === undefined || endY === undefined) return
        if (watermarkedImage.value === undefined) return
        
        const mask: Mask = { sx: startX, ex: endX, sy: startY, ey: endY }
        pixelStore.setPixelsWithMask(watermarkedImage.value, mask)  
        watermarkedImage.value = pixelStore.getFlatPixels()      
        activeImage.value = 'watermarked'
    }

    const resetWatermarks = (): void => {
        pixelStore.masks = []
        watermarkedImage.value = originalImage.value
        pixelStore.setPixels(originalImage.value!)
        activeImage.value = 'original'
    }

    const hasReconstructedImage: ComputedRef<boolean> = computed(() => recostructedImage.value !== undefined)

    return {
        activeImage,
        setActiveImage,
        setWithNewImage,
        setReconstructedImage,
        reset,
        isWatermarkingReady,
        watermarks,
        getWatermark,
        setWatermark,
        isWatermarkActive,
        addWatermark,
        resetWatermarks,
        hasReconstructedImage
    }
})