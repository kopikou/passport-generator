<script setup lang="ts">

import {computed, onBeforeMount, ref, watch} from "vue";
import PlanView from "components/PlanView.vue";
import DisciplineView from "components/DisciplineView.vue";
import DocumentsView from "components/DocumentsView.vue";
import CompetencesView from "components/CompetencesView.vue";
import IndicatorsView from "components/IndicatorsView.vue";
import SemesterView from "components/SemesterView.vue";
import {useQuasar} from "quasar";
import _ from "lodash";
import {api} from "boot/axios";
import usePlanViewStore from "stores/planViewStore";
import {storeToRefs} from "pinia";

const $q = useQuasar()

const props = defineProps({
  id: {
    required: true,
  }
})

const planViewStore = usePlanViewStore()
const {
  activeFileId,
  disabled,
} = storeToRefs(planViewStore);

const link = ref('plan')

function acceptPlan() {
  $q.dialog({
    title: 'Предупреждение',
    message: "<p style='font-size: 16px'>Вы уверены, что хотите синхронизировать план? <br/> В дальнейшем план нельзя будет изменить <br/> <span class='text-red-9'>Для продолжения введите \"Подтвердить\"</span></p>",
    cancel: {
      label: 'Отмена',
      flat: true,
    },
    ok: {
      label: 'Подтвердить',
      flat: true,
    },
    html: true,
    prompt: {
      model: '',
      isValid: val => val.toLowerCase() == 'подтвердить',
      type: "text",
    }
  }).onOk(async () => {
    let r = await api.get('api/upload/accept-file/', {params: {id: props.id}})
      .then(() => {
        $q.notify({
          color: "primary",
          type: 'secondary',
          message: `Успешно, отправляем данные в АИС! :)`,
        })
      })
    location.href = '/'
  })
}

watch(() => props.id,
  () => {
    activeFileId.value = props.id
  },
  {immediate: true})

</script>

<template>
  <div class="q-pt-md">
    <div v-show="disabled" class="text-center text-green text-h6">
      План отправлен в АИС, разрешен только просмотр
    </div>
    <div class="row">
      <div class="col-2">
        <q-list
          bordered
        >
          <q-item
            clickable
            v-ripple
            :active="link === 'plan'"
            @click="link = 'plan'"
            active-class="my-menu-link"
          >

            <q-item-section avatar>
              <q-icon name="mdi-book-edit-outline"/>
            </q-item-section>

            <q-item-section>План</q-item-section>

          </q-item>
          <q-item
            clickable
            v-ripple
            :active="link === 'disciple'"
            @click="link = 'disciple'"
            active-class="my-menu-link"
          >

            <q-item-section avatar>
              <q-icon name="mdi-account-school"/>
            </q-item-section>

            <q-item-section>Дисциплины</q-item-section>

          </q-item>
          <q-item
            clickable
            v-ripple
            :active="link === 'documents'"
            @click="link = 'documents'"
            active-class="my-menu-link"
          >

            <q-item-section avatar>
              <q-icon name="mdi-file-document-outline"/>
            </q-item-section>

            <q-item-section>Документы</q-item-section>

          </q-item>
          <q-item
            clickable
            v-ripple
            :active="link === 'semester'"
            @click="link = 'semester'"
            active-class="my-menu-link"
          >

            <q-item-section avatar>
              <q-icon name="mdi-clock-alert-outline"/>
            </q-item-section>

            <q-item-section>Семестры</q-item-section>

          </q-item>
          <q-item
            clickable
            v-ripple
            :active="link === 'indicators'"
            @click="link = 'indicators'"
            active-class="my-menu-link"
          >

            <q-item-section avatar>
              <q-icon name="mdi-invoice-check-outline"/>
            </q-item-section>

            <q-item-section>Индикаторы</q-item-section>

          </q-item>
        </q-list>

        <q-btn
          label="Отправить план в АИС"
          @click="acceptPlan"
          :disable="disabled"
          class="q-mt-md my-menu-link"
          style="width: 100%"
        />

      </div>
      <div class="col-10">
        <div class="q-pl-lg">
          <plan-view v-if="link === 'plan'"/>
          <discipline-view v-if="link === 'disciple'"/>
          <documents-view v-if="link === 'documents'"/>
          <semester-view v-if="link === 'semester'"/>
          <indicators-view v-if="link === 'indicators'"/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.my-menu-link {
  color: white;
  background: #F2C037;
}
</style>
