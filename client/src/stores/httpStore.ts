import { defineStore } from "pinia"
import { ComputedRef, Ref, computed, ref } from "vue"

export type ImagePayload = { x: number[], y: number[] }

export const useHttpStore = defineStore('http', () => {
    const isLoadingImages: Ref<boolean> = ref(false)
    const isFetching: ComputedRef<boolean> = computed(() => isLoadingImages.value)

    const loadImages = async (): Promise<ImagePayload | undefined> => {
        const headers = { 'Content-Type': 'application/json' }
        const method = 'GET'
        const options = { headers, method }
        const url = `${process.env.VUE_APP_GENERATE_ENDPOINT_URL}`
        const response: any = await request(url, options, 'Failed to load digit image.')
        if (response.error === undefined) return response
        alert(response.error)
        return undefined
    }

    const generateDigit = async (digit: number): Promise<number[] | undefined> => {
        const headers = { 'Content-Type': 'application/json' }
        const method = 'GET'
        const options = { headers, method }
        const url = `${process.env.VUE_APP_GENERATE_ENDPOINT_URL}?label=${digit}`
        const response: any = await request(url, options, 'Failed to generate digit.')
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

    return { loadImages, isFetching, isLoadingImages }
})
