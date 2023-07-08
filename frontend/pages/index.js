import Head from 'next/head'
import styles from '../styles/Home.module.css'
import {Button} from '@nextui-org/react';


export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="https://nextjs.org">Next.js</a> on Docker!
        </h1>
      </main>

      <footer className={styles.footer}>
      </footer>
    </div>
  )
}
