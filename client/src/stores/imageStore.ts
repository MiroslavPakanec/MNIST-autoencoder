import { defineStore } from "pinia"
import { ComputedRef, Ref, computed, ref } from "vue"
import { Mask, usePixelStore } from "./pixelStore"

export type Watermark = { w: number, h: number }

export const useImageStore = defineStore('image', () => {
    const pixelStore = usePixelStore()

    const originalImage: Ref<number[] | undefined> = ref(undefined)
    const watermarkedImage: Ref<number[] | undefined> = ref(undefined)
    const recostructedImage: Ref<number[] | undefined> = ref(undefined)

    const setWithNewImage = (image: number[]): void => {
        originalImage.value = image
        watermarkedImage.value = image
        recostructedImage.value = undefined
        pixelStore.setPixels(image)
    }

    const reset = (): void => {
        originalImage.value = undefined
        watermarkedImage.value = undefined
        recostructedImage.value = undefined
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
    }

    const resetWatermarks = (): void => {
        pixelStore.masks = []
        watermarkedImage.value = originalImage.value
        pixelStore.setPixels(originalImage.value!)
    }

    return {
        setWithNewImage,
        reset,
        isWatermarkingReady,
        watermarks,
        getWatermark,
        setWatermark,
        isWatermarkActive,
        addWatermark,
        resetWatermarks
    }
})