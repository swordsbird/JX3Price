import axios from 'axios'
import mongoose from 'mongoose'

mongoose.connect('mongodb://localhost/paopao', { useNewUrlParser: true })

const accountSchema = new mongoose.Schema({
    unparsed: Object,
    info: Object,
    url: String,
    price: Number,
    qq: String,
    name: String,
    timestamp: Number,
})
accountSchema.index('price')
accountSchema.index('url')

const accounts = mongoose.model('account', accountSchema)
const baseUrl = 'http://www.paopaox.com/zh.html?q=&page='
const basePenzaiUrl = 'https://www.j3dh.com/release/v1/dataHero?ifKnownDaishou=false&exterior=&filter=&school=0&figure=0&minPrice=&maxPrice=&ignorePriceFlag=true&ifNoDaishou=false'

async function fetchPaopao(index) {
    let body = await axios.get(baseUrl + index)
    let data = body.data
    let texts = data.split('<div class="arrText">').slice(1)
    texts[texts.length - 1] = texts[texts.length - 1].split('<div class="pageNav">')[0]
    let items = []
    for (let i = 20; i < texts.length; ++i) {
        let text = texts[i]
        try {
            const url = text.match(/<div class="text1"><a href="([^"]+)/)[1]
            const content = text.match(/class="text-hide" data-length=\d+>([^<]+)/)[1]
            let t = text.match(/class="copy qq" data-text="([^"]+)/)
            const qq = t && t[1] || 0
            const name = text.match(/class="avatar">([^<]+)/)[1]
            const time = text.match(/<i class="iconfont c3">&#xe6fb;<\/i>([^<]*)/)[1]
            let ts
            if (time.indexOf('分钟前')) {
                ts = new Date()  - parseInt(time) * 60 * 1000
            } else if (time.indexOf('小时前')) {
                ts = new Date()  - parseInt(time) * 3600 * 1000
            } else if (time.indexOf('天前')) {
                ts = new Date()  - parseInt(time) * 24 * 3600 * 1000
            } else {
                let date = text.match(/\(([^\)]+)/)
                if (date) {
                    date = new Date(`2019-${date}`)
                } else {
                    date = new Date()
                }
                ts = +date
            }
            items.push({ unparsed: { content, time }, url, qq, name, timestamp: ts })
        } catch (e) {
            console.log(text)
            continue
        }
    }
    let counter = 0
    for (let item of items) {
        const status = await accounts.findOne({ url: item.url })
        if (status) {
            continue
        }
        counter++
        const x = new accounts(item)
        await x.save()
    }
    console.log(`page ${index}, ${counter} items have been parsed.`)
    return counter == 0
}

let time

async function fetchPenzai(index) {
    let body = await axios.get(`${basePenzaiUrl}&page=${index}&sinceTime=${Math.floor(time/1000-86400*30)}&time=${time}`)
    let data = body.data.Result
    let items = []
    for (let x of data.Heros) {
        try {
            const url = x.id
            const content = x.content
            const qq = x.user_qq
            const name = x.user_name
            const time = 'parsed'
            const ts = +new Date(x.update_time) || 0
            if (ts == 0) {
                console.log(x)
            } else {
                items.push({ unparsed: { content, time }, url, qq, name, timestamp: ts })
            }
        } catch (e) {
            console.log(x)
        }
    }
    let counter = 0
    for (let item of items) {
        const status = await accounts.findOne({ url: item.url })
        if (status) {
            continue
        }
        counter++
        const x = new accounts(item)
        await x.save()
    }
    console.log(`page ${index}, ${counter} items have been parsed.`)
    return counter == 0
}

async function getPenzaiLen() {
    let body = await axios.get(`${basePenzaiUrl}&page=0&sinceTime=${Math.floor(time/1000-86400*30)}&time=${time}`)
    let data = body.data
    let total = data.Result.Total
    return total
}

async function main() {
    time = +new Date()
    let len = await getPenzaiLen()

    for (let i = 30000; i < 40000; i += 20) {
        await fetchPenzai(i)
    }

    for (let i = 0; i < 1300; ++i) {
        const status = await fetchPaopao(i)
    }
}

main()
