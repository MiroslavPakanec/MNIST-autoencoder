import { defineStore } from "pinia"
import { ComputedRef, Ref, computed, ref } from "vue"
import { usePixelStore } from "./pixelStore"

type WatermarkShape = { w: number, h: number }

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

    const watermarks: Ref<WatermarkShape[]> = ref([
        { w: 2, h: 12 },
        { w: 12, h: 2 },
        { w: 8, h: 4 },
        { w: 4, h: 8 },
    ])

    const activeWatermarkIndex: Ref<number> = ref(0)
    const getWatermark = (): [number, number] => [ watermarks.value[activeWatermarkIndex.value].w, watermarks.value[activeWatermarkIndex.value].h ]
    const setWatermark = (index: number) => activeWatermarkIndex.value = index
    const isWatermarkActive = (index: number) => activeWatermarkIndex.value === index

    return {
        setWithNewImage,
        reset,

        isWatermarkingReady,
        watermarks,
        getWatermark,
        setWatermark,
        isWatermarkActive
    }
})