import { defineStore } from "pinia"
import { ComputedRef, Ref, computed, ref } from "vue"
import { usePixelStore } from "./pixelStore"

export type ImagePayload = { x: number[], y: number[] }
export type PredictImagePayload = { experiment_id: string, sample: number[] }
export type PredictedImagePayload = { y: number[] }
export type WatermarkPayload = [number, number][]

export const useHttpStore = defineStore('http', () => {
    const isLoadingImages: Ref<boolean> = ref(false)
    const isFetching: ComputedRef<boolean> = computed(() => isLoadingImages.value)

    const loadWatermarks = async (): Promise<WatermarkPayload | undefined> => {
        const headers = { 'Content-Type': 'application/json' }
        const method = 'GET'
        const options = { headers, method }
        const url = `${process.env.VUE_APP_LOAD_WATERMARKS_ENDPOINT_URL}`
        const response: any = await request(url, options, 'Failed to load digit image.')
        if (response.error === undefined) return response
        alert(response.error)
        return undefined
    }

    const loadImages = async (): Promise<ImagePayload | undefined> => {
        const headers = { 'Content-Type': 'application/json' }
        const method = 'GET'
        const options = { headers, method }
        const url = `${process.env.VUE_APP_LOAD_IMAGE_ENDPOINT_URL}`
        const response: any = await request(url, options, 'Failed to load digit image.')
        if (response.error === undefined) return response
        alert(response.error)
        return undefined
    }

    const predictImage = async (pixels: number[]): Promise<PredictedImagePayload | undefined> => {
        const headers = { 'Content-Type': 'application/json' }
        const method = 'POST'

        const experimentId: string = process.env.VUE_APP_EXPERIMENT_ID
        const payload: PredictImagePayload = { experiment_id: experimentId, sample: pixels }
        const body: string = JSON.stringify(payload)

        const options = { headers, method, body }
        const url = `${process.env.VUE_APP_PREDICT_IMAGE_ENDPOINT_URL}`
        const response: any = await request(url, options, 'Failed to load digit image.')
        if (response.error === undefined) return response
        alert(response.error)
        return undefined
    }

    const request = async (url: string, options: any, errorMessage?: string): Promise<any> => {
        try {
            isLoadingImages.value = true
            const response: any = await fetch(url, options)
            if (response?.ok) return await response.json()
            else return { error: (await response.json())?.error ?? errorMessage ?? 'Something went wrong' }
        } catch (error: any) {
            console.log(error)
            return { error: errorMessage ?? error.message ?? 'Something went wrong' }
        } finally {
            isLoadingImages.value = false
        }
    }

    return { loadImages, loadWatermarks, predictImage, isFetching, isLoadingImages }
})
