import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios"

const urlprefix = "http://jx3.in"
const typeOrder = [
  "点月",
  "体型",
  "门派",
  "红发",
  "金发",
  "五限",
  "六限",
  "包身盒子",
  "普通盒子",
  "限时",
  "复刻",
  "披风",
  "挂宠",
  "奇遇",
  "其他",
  "统计"
]
const typeGroupCounts = [['基本', 3], ['发型', 2], ['限量', 2], ['盒子', 2], ['限时', 1], ['复刻', 1], ['披风', 1], ['挂宠', 1], ['其他', 2], ["统计", 1]]
const cntAccepted = {
    '下架': [0, 100],
    '成衣': [0, 300],
    '白发': [0, 100],
    '黑发': [0, 100],
    '五甲': [0, 300],
    '奇趣': [0, 50],
    '拓印': [0, 100],
    '脚印': [0, 15],
    '宠物': [0, 11000],
    '资历': [0, 120000],
}
Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        rawitems: [],
        items: [],
        typedItems: {},
        typeGroups: [],
        current: null,
        report: null,
        history: [],
        waitingForResponse: false,
        showAlert: false,
        useClassicFont: false,
        useFullName: false,
        links: [
            { title: 'text', text: '详情估价', icon: 'mdi-message', route:"/text" },
            { title: 'customize', text: '自选外观', icon: 'mdi-view-list', route:"/customize" },
            { title: 'history', text: '历史信息', icon: 'mdi-history', route:"/history" },
            { title: 'analysis', text: '翻车货！', icon: 'mdi-money-off', route:"/analysis" },
        ],
    },
    getters: {
        links: state => state.links,
        typeGroups: state => state.typeGroups,
        last: state => state.history.length && state.history[state.history.length - 1],
        isLoading: state => state.waitingForResponse,
        useClassicFont: state => state.useClassicFont,
        useFullName: state => state.useFullName,
    },
    mutations: {
        addReport(state, { v, school, body, price, time }) {
            let userProps = v.map((d, i) => [d, i])
                .filter(d => d[0] && state.rawitems[d[1]].price0 != 0)
                .map(d => ({
                    name: state.rawitems[d[1]].name,
                    price: state.rawitems[d[1]].price,
                    price0: state.rawitems[d[1]].price0,
                    index: d[1],
                    value: d[0],
                }))
            let totalPrice = userProps.map(d => d.price * d.value).reduce((a, b) => a + b, 0)
            let totalPrice0 = userProps.map(d => d.price0 * d.value).reduce((a, b) => a + b, 0)
            state.report = { summary: { v, school, body, price, time }, userProps, totalPrice, totalPrice0 }
            console.log(state.report)
        },
        addHistory(state, { v, school, body, price, time }) {
            if (!time) time = new Date()
            v = v.slice(0)
            state.history.push({v, school, body, price, time })
        },
        addAccount(state, { v, school, body, price }) {
            v = v || []
            school = school || null
            body = body || null
            price = price || null
            state.current = { v, school, body, price }
            if (state.current.v.length == 0) {
                for (let x of state.items) {
                    state.current.v.push(0)
                }
            }
        },
        changeCurrentValue(state, index) {
            if (state.rawitems[index].type == '门派') {
                for (let x of state.typedItems['门派']) {
                    state.current.v[x.index] = 0
                }
                state.current.v[index] = 1
                state.current.school = state.rawitems[index].name
            } else if (state.rawitems[index].type == '体型') {
                for (let x of state.typedItems['体型']) {
                    state.current.v[x.index] = 0
                }
                state.current.v[index] = 1
                state.current.body = state.rawitems[index].name
            } else {
                state.current.v[index] = 1 - state.current.v[index]
            }
        },
        changeCurrentValueTo(state, { index, value }) {
            state.current.v[index] = value
        },
        changeGroupValue(state, type) {
            if (!state.typedItems[type]) return
            let sum = 0
            for (let x of state.typedItems[type]) {
                sum += state.current.v[x.index] || 0
            }
            let y = sum == state.typedItems[type].length ? 0 : 1
            for (let x of state.typedItems[type]) {
                state.current.v[x.index] = y
            }
        },
        setCurrentValue(state, payload) {
            let { school, body, price, v } = payload
            if (school) state.current.school = school
            if (body) state.current.body = body
            if (price) state.current.price = price
            if (v) {
                state.current.v = v
            }
        },
        setItems(state, items) {
            let typerank = {}
            for (let i = 0; i < typeOrder.length; ++i) {
                typerank[typeOrder[i]] = i + 1
            }
            for (let x of items) if (!typerank[x.type]) {
                typerank[x.type] = 100
            }

            items = items.sort((a, b) => {
                if (typerank[a.type] != typerank[b.type]) {
                    return typerank[a.type] - typerank[b.type]
                } else if (a.date != b.date) {
                    return a.date < b.date ? -1 : 1
                } else {
                    return a.index - b.index
                }
            })
            state.rawitems = items.slice(0).sort((a, b) => a.index - b.index)
            state.items = items

            state.typedItems = {}
            for (let x of state.items) {
                if (!state.typedItems[x.type]) {
                    state.typedItems[x.type] = []
                }
                state.typedItems[x.type].push(x)
            }

            let types = Object.keys(state.typedItems)
            let counter = 0
            for (let k of typeGroupCounts) {
                let group = []
                for (let i = counter; i < counter + k[1]; ++i) {
                    group.push({ name: types[i], index: i, items: state.typedItems[types[i]]})
                }
                let name = k[0]
                if (counter >= 5 && counter <= 12) {
                    let gitems = [].concat(...group.map(d => d.items))
                    gitems = gitems.sort((a, b) => a.date < b.date ? -1 : 1)
                    group = []
                    let dates = []
                    let dateset = new Set()
                    for (let x of gitems) if (!dateset.has(x.date.slice(0,7))) {
                        dateset.add(x.date.slice(0,7))
                        dates.push(x.date.slice(0,7))
                    }
                    dates = dates.map(d => ({ date: d, items: [] }))
                    let datemap = {}
                    dates.forEach(d => datemap[d.date.slice(0,7)] = d)
                    for (let x of gitems) {
                        datemap[x.date.slice(0,7)].items.push(x)
                    }
                    let yearset = new Set()
                    let newdates = []
                    for (let x of dates) {
                        if (x.date == '2020/12') {
                            newdates.push({ date: `其他`, items: x.items, timepoint: false })
                        } else {
                            let year = x.date.split('/')[0]
                            let month = x.date.split('/')[1]
                            if (!yearset.has(year)) {
                                yearset.add(year)
                                newdates.push({ date: `${year}年`, timepoint: true })
                            }
                            newdates.push({ date: `${month}月`, items: x.items, timepoint: false })
                        }
                    }
                    state.typeGroups.push({
                        name: name,
                        group: newdates,
                        timeline: true,
                    })
                } else {
                    if (group[0].name == '统计') {
                        group[0].items = group[0].items
                            .filter(d => !!cntAccepted[d.name])
                        group[0].range = group[0].items.map(d => cntAccepted[d.name])
                    }
                    state.typeGroups.push({
                        name: name,
                        group: group,
                        timeline: false,
                    })
                }
                counter += k[1]
            }
        },
        waitingEnd(state) {
            state.waitingForResponse = false
        },
        waiting(state) {
            state.waitingForResponse = true
        },
        sendAlert(state) {
            state.showAlert = true
        },
        closeAlert(state) {
            state.showAlert = false
        },
        changeClassicFont(state) {
            state.useClassicFont = !state.useClassicFont
        },
        changeFullName(state) {
            state.useFullName = !state.useFullName
        }
    },
    actions: {
        async init({ commit }) {
            const res = await axios.get(`${urlprefix}/api/items`)
            const data = res.data
            const items = data.items
            commit('setItems', items)
            commit('addAccount', {})
        },
        addAnalysisReport({ commit }, data){
            commit('addReport', data)
        },
        changeValue({ commit }, index) {
            commit('changeCurrentValue', index)
        },
        changeValueTo({ commit }, { index, value }) {
            commit('changeCurrentValueTo', { index, value })
        },
        changeGroupValue({ commit }, name) {
            commit('changeGroupValue', name)
        },
        changeClassicFont({ commit }) {
            commit('changeClassicFont')
        },
        changeFullName({ commit }) {
            commit('changeFullName')
        },
        changeAccount({ commit }, x) {
            if (x) {
                commit('addAccount', {
                    v: x.v.slice(0),
                    school: x.school,
                    body: x.body,
                })
            }
        },
        async queryPriceByText({ commit }, text) {
            commit('waiting')
            try {
                const res = await axios.post(`${urlprefix}/api/queryaccount/`, { text })
                const data = res.data
                commit('addHistory', {
                    price: data.price,
                    v: data.v,
                    school: data.school,
                    body: data.body
                })
            } catch(e) {
                console.log(e)
                commit('sendAlert')
            }
            commit('waitingEnd')
        },
        async queryCurrentPrice({ state, commit }) {
            commit('waiting')
            try {
                const res = await axios.post(`${urlprefix}/api/queryaccount/`, {
                    v: state.current.v,
                    body: state.current.body,
                    school: state.current.school,
                })
                const data = res.data
                commit('setCurrentValue', { price: data.price, v: data.vector })
                commit('addHistory', state.current)
            } catch(e) {
                commit('sendAlert')
            }
            commit('waitingEnd')
        },
    }
})