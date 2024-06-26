import { defineStore } from "pinia"
import { Ref, ref } from "vue"

export const useColorStore = defineStore('color', () => {
    const primary: Ref<string> = ref('rgb(189, 81, 107)')
    const secondary: Ref<string> = ref('rgb(36, 7, 80)')
    const ternary: Ref<string> = ref('rgb(202, 202, 202)')

    return {
        primary,
        secondary,
        ternary
    }
})