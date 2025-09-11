import {defineStore} from "pinia";

const useRulesStore = defineStore("RulesStore", () => {
  const required = (message = 'Заполните данное поле') => (val) =>
    !!val || message

  const positiveNumber = (message = 'Число должно быть положительным') => (val) =>
    (val > 0) || message

  const maxNumber = (max = 5, message = `Число должно быть меньше или равно ${max}`) => (val) =>
    (val <= max) || message

  return {
    required,
    positiveNumber,
    maxNumber,
  }
})

export default useRulesStore;
